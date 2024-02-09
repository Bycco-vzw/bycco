# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, Optional, List
from datetime import date, datetime, timezone, timedelta
from fastapi import BackgroundTasks

from reddevil.core import get_settings, RdBadRequest, RdInternalServerError

from bycco.lodging.md_lodging import (
    Assignment,
    Guest,
    DbLodging,
    Lodging,
    LodgingIn,
)
from bycco.room import Room, get_room_by_number, update_room

# from bycco.room import Room
# from bycco.service.room import update_room

from bycco.core.mail import sendemail_reservation
from bycco.core.counter import DbCounter
from bycco.core.common import get_common
from bycco.main import settings

logger = logging.getLogger(__name__)
settings = get_settings()
common = get_common()
startdate = common["period"]["startdate"]
enddate = common["period"]["enddate"]
m3y = date(startdate.year - 3, startdate.month, startdate.day)
m12y = date(startdate.year - 12, startdate.month, startdate.day)
m18y = date(startdate.year - 18, startdate.month, startdate.day)


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


async def make_reservation(d: LodgingIn, bt: BackgroundTasks) -> str:
    rd = d.model_dump()
    logger.info(f"rd {rd}")
    rd["locale"] = rd.get("locale") or "nl"
    rd["lodging"] = rd.get("lodging") or settings.DEFAULT_LODGING
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
        gd["lodging"] = rd["lodging"]
        gl.append(gd)
    rd["guestlist"] = gl
    rd["enabled"] = True
    rd["organizers"] = False if rd.get("organizers") is None else rd["organizers"]
    rd["number"] = await DbCounter.next("reservation")
    logger.info(f"call add Reservation {rd}")
    try:
        id = await DbLodging.add(rd)
    except:
        logger.exception("Cannot add rsv")
        raise RdInternalServerError("Cannot add rsv")
    logger.info(
        f"Reservation {id} registered for {rd['first_name']} {rd['last_name']} "
    )
    try:
        ldg = await get_lodging(id)
        logger.info(f"saved lodging {ldg}")
    except:
        logger.exception("Cannot get lodging")
        raise RdInternalServerError("Cannot get added rsv")
    logger.info("calling sendReservation")
    bt.add_task(sendemail_reservation, ldg)
    return id


async def get_lodging(id: str, options: dict = {}) -> Lodging:
    """
    get the Lodging
    """
    filter = options.copy()
    filter["id"] = id
    filter["_model"] = filter.pop("_model", Lodging)
    return cast(Lodging, await DbLodging.find_single(filter))


async def get_lodgings(options: dict = {}) -> List[Lodging]:
    """
    get the reservations
    """
    filter = options.copy()
    filter["_model"] = filter.pop("_model", Lodging)
    return [cast(Lodging, x) for x in await DbLodging.find_multiple(filter)]


async def update_lodging(id: str, rsv: Lodging, options: dict = {}) -> Lodging:
    opt = options.copy()
    opt["_model"] = opt.pop("_model", Lodging)
    lodging = cast(
        Lodging, await DbLodging.update(id, rsv.model_dump(exclude_unset=True), opt)
    )
    return lodging


async def assign_room(
    id: str,
    roomnr: str,
) -> Lodging:
    """
    assign a room to a reservation
    """

    reservation = await get_lodging(id)
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
    return await update_lodging(id, Lodging(assignments=assignments, logging=logging))


async def unassign_room(id: str, roomnr: str) -> Lodging:
    """
    unassign a room to a reservation
    """

    reservation = await get_lodging(id)
    room = await get_room_by_number(roomnr)
    now = datetime.now(tz=timezone.utc)
    assignments = [a for a in (reservation.assignments or []) if a.roomnr != roomnr]
    await update_room(room.id, Room(reservation_id=None, reservation_nr=None))
    logging = reservation.logging or []
    nf = now.isoformat(sep=" ", timespec="minutes")
    logging.append(f"{nf} Unassigned room {roomnr} to reservation {reservation.number}")
    return await update_lodging(id, Lodging(assignments=assignments, logging=logging))


async def xls_lodgings() -> bytes:
    """
    get all reservations in xls format
    """
    # docs = await DbLodging.find_multiple()
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
