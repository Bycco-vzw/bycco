# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, List
from datetime import date, datetime, timezone, timedelta
from fastapi import BackgroundTasks
from tempfile import NamedTemporaryFile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import openpyxl


from reddevil.core import get_settings, RdBadRequest, RdInternalServerError
from bycco.core.counter import DbCounter
from bycco.core.common import load_common


from . import (
    Assignment,
    DbStay,
    Stay,
    StayIn,
)
from bycco.room import Room, get_room_by_number, update_room


logger = logging.getLogger(__name__)
settings = get_settings()

common = None
startdate = None
enddate = None
m3y = None
m12y = None
m18y = None


async def get_stay(id: str, options: dict = {}) -> Stay:
    """
    get the Stay
    """
    filter = options.copy()
    filter["id"] = id
    filter["_model"] = filter.pop("_model", Stay)
    return cast(Stay, await DbStay.find_single(filter))


async def get_stays(options: dict = {}) -> List[Stay]:
    """
    get the reservations
    """
    filter = options.copy()
    filter["_model"] = filter.pop("_model", Stay)
    return [cast(Stay, x) for x in await DbStay.find_multiple(filter)]


async def update_stay(id: str, rsv: Stay, options: dict = {}) -> Stay:
    opt = options.copy()
    opt["_model"] = opt.pop("_model", Stay)
    stay = cast(Stay, await DbStay.update(id, rsv.model_dump(exclude_unset=True), opt))
    return stay


def loopdays():
    """
    return a list of days from startdate - 1 to enddate + 1
    """
    ndays = (enddate - startdate).days + 3
    return [startdate + timedelta(days=i - 1) for i in range(ndays)]


def calcmeals(cid: date, cod: date, meals: str):
    """
    return a list of meals in format of MM-DD-[B,L,D]
    cid: checkindate
    cod: checkoutdate
    """
    if meals == "no":
        return []
    ml = []
    for d in loopdays():
        if d == cid:
            ml.append(f"{d:%m-%d}-D")
        if cid < d < cod:
            ml.append(f"{d:%m-%d}-B")
            if meals == "full":
                ml.append(f"{d:%m-%d}-L")
            ml.append(f"{d:%m-%d}-D")
        if d == cod:
            ml.append(f"{d:%m-%d}-B")
    return ml


def sendemail_reservation(stay: Stay):
    from bycco.core.mail import (
        backends,
        env,
        md,
        markdownstyle,
    )

    logger.info(f"sending reservation email {stay}")
    tmpl = env.get_template(f"mailreservation_{stay.locale}.md")
    context = stay.model_dump()
    logger.info(f"context: {context}")
    # translate
    for r in common["rooms"]:
        if r["name"] == stay.stay:
            break
    context["stay"] = r[stay.locale]
    i18n = common["i18n"]
    context["meals"] = i18n[stay.meals][stay.locale]
    # render the content using jinja2 templating giving markdown text
    markdowntext = tmpl.render(**context)
    # convert markdown text to html
    htmltext = f"{markdownstyle} {md.convert(markdowntext)}"
    try:
        sender = settings.EMAIL["sender"]
        receiver = stay.email
        msg = MIMEMultipart("related")
        msg["Subject"] = "Floreal 2025"
        msg["From"] = sender
        msg["To"] = receiver
        if settings.EMAIL.get("bcc_reservation"):
            msg["Bcc"] = settings.EMAIL["bcc_reservation"]
        msg.preamble = "This is a multi-part message in MIME format."
        msgAlternative = MIMEMultipart("alternative")
        msgText = MIMEText(markdowntext)
        msgAlternative.attach(msgText)
        msgText = MIMEText(htmltext, "html")
        msgAlternative.attach(msgText)
        msg.attach(msgAlternative)
        backend = backends[settings.EMAIL["backend"]]()
        backend.send_message(msg)
        logger.info(f"reservation email sent to {receiver}")
    except Exception:
        logger.exception("failed")


async def setup_globals():
    global common, startdate, enddate, m12y, m3y, m18y
    if not common:
        common = await load_common()
        startdate = common["trndates"]["startdate"]
        enddate = common["trndates"]["enddate"]
        m3y = date(startdate.year - 3, startdate.month, startdate.day)
        m12y = date(startdate.year - 12, startdate.month, startdate.day)
        m18y = date(startdate.year - 18, startdate.month, startdate.day)


async def make_reservation(d: StayIn, bt: BackgroundTasks) -> str:
    await setup_globals()
    rd = d.model_dump()
    logger.info(f"rd {rd}")
    rd["locale"] = rd.get("locale") or "nl"
    rd["stay"] = rd.get("stay") or settings.DEFAULT_LODGING
    rd["meals"] = rd.get("meals") or settings.DEFAULT_MEALS
    gl = []
    try:
        cid = date.fromisoformat(d.checkindate[:10])
        cod = date.fromisoformat(d.checkoutdate[:10])
    except ValueError:
        raise RdBadRequest(description="Invalid date format")
    for gd in rd["guestlist"]:
        gd["meals"] = calcmeals(cid, cod, rd["meals"])
        try:
            bdate = date.fromisoformat(gd["birthdate"])
        except ValueError:
            raise RdBadRequest(description="Invalid birthdatedate format")
        age_category = "Adult"
        if bdate > m18y:
            age_category = "-18"
        if bdate > m12y:
            age_category = "-12"
        if bdate > m3y:
            age_category = "-3"
        gd["age_category"] = age_category
        gd["stay"] = rd["stay"]
        gl.append(gd)
    rd["guestlist"] = gl
    rd["enabled"] = True
    rd["organizers"] = False if rd.get("organizers") is None else rd["organizers"]
    rd["number"] = await DbCounter.next("reservation")
    logger.info(f"call add Reservation {rd}")
    try:
        id = await DbStay.add(rd)
    except Exception:
        logger.exception("Cannot add rsv")
        raise RdInternalServerError("Cannot add rsv")
    logger.info(
        f"Reservation {id} registered for {rd['first_name']} {rd['last_name']} "
    )
    try:
        ldg = await get_stay(id)
        logger.info(f"saved stay {ldg}")
    except Exception:
        logger.exception("Cannot get stay")
        raise RdInternalServerError("Cannot get added rsv")
    logger.info("calling sendReservation")
    bt.add_task(sendemail_reservation, ldg)
    return id


async def assign_room(
    id: str,
    roomnr: str,
) -> Stay:
    """
    assign a room to a reservation
    """
    await setup_globals()
    reservation = await get_stay(id)
    room = await get_room_by_number(roomnr)
    if room.reservation_id is not None:
        logger.info(f"cannot assign {roomnr}: already taken")
        raise RdBadRequest(description="RoomAlreadyTaken")
    if room.blocked:
        logger.info(f"cannot assign {roomnr}: blocked")
        raise RdBadRequest(description="RoomBlocked")
    now = datetime.now(tz=timezone.utc)
    assignments = reservation.assignments or []
    assignments.append(
        Assignment(
            roomnr=roomnr,
            roomtype=room.roomtype,
            guestlist=reservation.guestlist,
            assignmentdate=now,
        )
    )
    await update_room(
        room.id, Room(reservation_id=id, reservation_nr=reservation.number)
    )
    logging = reservation.logging or []
    nf = now.isoformat(sep=" ", timespec="minutes")
    logging.append(f"{nf} Assigned room {roomnr} to reservation {reservation.number}")
    return await update_stay(id, Stay(assignments=assignments, logging=logging))


async def unassign_room(id: str, roomnr: str) -> Stay:
    """
    unassign a room to a reservation
    """
    await setup_globals()
    reservation = await get_stay(id)
    room = await get_room_by_number(roomnr)
    now = datetime.now(tz=timezone.utc)
    assignments = [a for a in (reservation.assignments or []) if a.roomnr != roomnr]
    await update_room(room.id, Room(reservation_id=None, reservation_nr=None))
    logging = reservation.logging or []
    nf = now.isoformat(sep=" ", timespec="minutes")
    logging.append(f"{nf} Unassigned room {roomnr} to reservation {reservation.number}")
    return await update_stay(id, Stay(assignments=assignments, logging=logging))


async def xls_stays() -> bytes:
    """
    get all reservations in xls format
    """
    await setup_globals()
    docs = await DbStay.find_multiple({"_model": Stay})
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reservations"
    ws.append(
        [
            "number",
            "first_name",
            "last_name",
            "email",
            "enabled",
            "checkindate",
            "checkoutdate",
            "address",
            "locale",
            "meals",
            "roomnr",
            "roomtype",
            "payment_id",
            "remarks",
            "bycco_remarks",
        ]
    )
    for d in docs:
        ws.append(
            [
                d.number,
                d.first_name,
                d.last_name,
                d.email,
                d.enabled,
                str(d.checkindate)[0:10],
                str(d.checkoutdate)[0:10],
                d.address,
                d.locale,
                d.meals,
                d.assignments[0].roomnr if d.assignments else "",
                d.assignments[0].roomtype if d.assignments else "",
                d.payment_id,
                d.remarks,
                d.bycco_remarks,
            ]
        )
    wsguests = wb.create_sheet("Guests")
    wsguests.append(
        [
            "number",
            "first_name",
            "last_name",
            "birthdate",
            "player",
            "age_category",
            "stay",
            "meals",
        ]
    )
    for d in docs:
        if not d.enabled:
            continue
        for g in d.guestlist:
            wsguests.append(
                [
                    d.number,
                    g.first_name,
                    g.last_name,
                    g.birthdate,
                    g.player,
                    g.age_category,
                    g.stay,
                    ",".join(g.meals) if g.meals else "",
                ]
            )
    with NamedTemporaryFile() as tmp:
        wb.save(tmp.name)
        tmp.seek(0)
        xlscontent = tmp.read()
    logger.info(f"xlscontent {len(xlscontent)}")
    return xlscontent
    # guestdocs = []
    # assigndocs = []
    # for d in docs:
    #     d.pop("_version", None)
    #     d.pop("_DocumentType", None)
    #     d.pop("logging", None)
    #     guests = d.pop("guestlist", [])
    #     for g in guests:
    #         guestdocs.append(dict(g, number=d["number"], id=d["id"]))
    #     assignments = d.pop("assignments", [])
    #     for a in assignments:
    #         assigndocs.append(dict(a, number=d["number"], id=d["id"]))
    # dfr = pd.DataFrame.from_records(docs)
    # dfg = pd.DataFrame.from_records(guestdocs)
    # dfa = pd.DataFrame.from_records(assigndocs)
    # bio = io.BytesIO()
    # with pd.ExcelWriter(bio) as writer:
    #     dfr.to_excel(writer, sheet_name="Reservations")
    #     dfg.to_excel(writer, sheet_name="Guests")
    #     dfa.to_excel(writer, sheet_name="Assignments")
    # b = bio.getvalue()
    # log.info(f"len {len(b)}")
    # return b
