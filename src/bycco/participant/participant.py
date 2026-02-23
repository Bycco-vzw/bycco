# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, List
from binascii import a2b_base64
from fastapi import Response
from jinja2 import PackageLoader, Environment
import openpyxl
from tempfile import NamedTemporaryFile

from reddevil.core import RdBadRequest, RdNotFound
from bycco.participant import (
    ParticipantCategory,
    ParticipantDetail,
    ParticipantItem,
    ParticipantUpdate,
    Participant,
    DbParticipant,
    Gender,
)
from bycco.registration import (
    Registration,
    get_registration,
    get_registrations,
    lookup_idbel,
    lookup_idfide,
)

logger = logging.getLogger(__name__)
tmpl_env = Environment(loader=PackageLoader("bycco"), trim_blocks=True)


async def get_participants(options: dict | None = None) -> List[ParticipantItem]:
    filter = options.copy() if options else {}
    filter["_model"] = filter.pop("_model", ParticipantItem)
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["_fieldlist"].append("_creationtime")
    logger.info(f"get_participants {filter}")
    pars = list(await DbParticipant.find_multiple(filter))
    return pars


async def get_participant(id: str) -> ParticipantDetail:
    filter: dict = {"_model": ParticipantDetail}
    filter["_fieldlist"] = list(ParticipantDetail.model_fields.keys())
    filter["_fieldlist"].append("_creationtime")
    filter["id"] = id
    par = await DbParticipant.find_single(filter)
    return par


async def get_participant_by_idbel(idbel: str) -> ParticipantItem:
    filter: dict = {"_model": ParticipantItem}
    filter["_fieldlist"] = list(ParticipantItem.model_fields.keys())
    filter["idbel"] = idbel
    return await DbParticipant.find_single(filter)


async def create_participant(idbel: str, category: ParticipantCategory) -> None:
    """
    create a participant
    """
    pl = await lookup_idbel(idbel)
    return await DbParticipant.add(
        {
            "badgemimetype": "",
            "badglength": 0,
            "badgeimage": None,
            "birthyear": pl.birthyear,
            "category": category,
            "chesstitle": pl.chesstitle or "",
            "enabled": True,
            "emails": [],
            "first_name": pl.first_name,
            "gender": pl.gender,
            "idbel": idbel,
            "idclub": pl.idclub,
            "idfide": pl.idfide,
            "locale": "nl",
            "last_name": pl.last_name,
            "nationalityfide": pl.nationalityfide,
            "ratingbel": pl.ratingbel,
            "ratingfide": pl.ratingfide,
            "remarks": "late registration",
        }
    )


async def import_registration(idreg) -> str:
    """
    import an enrollemnt and create a participant
    return the id of the participant
    """
    reg = cast(Registration, await get_registration(idreg, {"_model": Registration}))
    return await DbParticipant.add(
        {
            "badgeimage": reg.badgeimage,
            "badgemimetype": reg.badgemimetype,
            "badgelength": reg.badgelength,
            "birthyear": reg.birthyear,
            "category": ParticipantCategory(reg.category.value),
            "chesstitle": reg.chesstitle or "",
            "enabled": True,
            "emails": reg.emailplayer.split(",")
            + reg.representative.emailparent.split(",")
            + reg.representative.emailattendant.split(","),
            "first_name": reg.first_name,
            "gender": Gender(reg.gender) if reg.gender else None,
            "idbel": reg.idbel,
            "idclub": reg.idclub,
            "idfide": reg.idfide,
            "locale": reg.locale,
            "last_name": reg.last_name,
            "nationalityfide": reg.nationalityfide,
            "natstatus": reg.natstatus,
            "present": None,
            "ratingbel": reg.ratingbel or 0,
            "ratingfide": reg.ratingfide or 0,
            "remarks": "",
        }
    )


async def import_regitrations():
    """
    import all registration for the bjk 2025
    check doubles5
    retain most recent registration for the same person
    """
    regs = await get_registrations({"confirmed": True, "enabled": True})
    idbels = {}
    for reg in regs:
        if reg.idbel in idbels:
            # we have a double detected via idbel
            if reg.registrationtime > idbels[reg.idbel].registrationtime:
                idbels[reg.idbel] = reg  # keep most recent
        else:
            idbels[reg.idbel] = reg
    # process the participants
    for idbel, reg in idbels.items():
        try:
            par = await get_participant_by_idbel(idbel)
        except RdNotFound:
            par = None
        if par is None:
            await import_registration(reg.id)


async def update_participant(
    id: str, par: ParticipantUpdate, options: dict = {}
) -> Participant:
    opt = options.copy()
    opt["_model"] = opt.pop("_model", ParticipantDetail)
    upd = par.model_dump(exclude_unset=True)
    return cast(
        Participant,
        await DbParticipant.update(id, upd, opt),
    )


async def update_elo() -> None:
    """
    update the elo of all participants
    """
    prts = await get_participants()
    for pr in prts:
        if not pr.enabled:
            continue
        logger.info(f"updating elo {pr.last_name} {pr.first_name}")
        upd = Participant()
        if pr.idbel and pr.idbel != "0":
            try:
                pl = await lookup_idbel(pr.idbel)
                upd.ratingbel = pl.ratingbel
                upd.idclub = pl.idclub
            except Exception as e:
                logger.info(f"lookup idbel failed {pr.last_name} {pr.first_name}: {e}")
        if pr.idfide and pr.idfide != "0":
            try:
                pl = await lookup_idfide(pr.idfide)
                upd.ratingfide = pl.ratingfide
            except Exception as e:
                logger.info(f"lookup idfide failed {pr.last_name} {pr.first_name}: {e}")
        if upd:
            await update_participant(pr.id, upd)


async def generate_badges(cat: str = "", ids: str = "", orgids: str = ""):
    """
    get the Namecards for the bjk by categorie or by ids
    cat: str
    ids: comma separated ids
    """
    logger.info(f"generate_badges cat={cat} ids={ids}")
    if cat:
        prts = await get_participants({"category": cat, "enabled": True})
    elif ids:
        prts = await get_participants(
            {"idbel": {"$in": ids.split(",")}, "enabled": True}
        )
    elif orgids:
        prts = await get_participants(
            {"orgid": {"$in": orgids.split(",")}, "enabled": True}
        )

    else:
        prts = await get_participants({"meals": {"$ne": None}, "enabled": True})
    logger.info(f"nr of participants {len(prts)}")
    pages = []
    badges = []
    j = 0
    sorteddocs = sorted(prts, key=lambda x: f"{x.last_name}, {x.first_name}")
    for ix, p in enumerate(sorteddocs):
        rix = j % 2 + 1
        cix = j // 2 + 1
        badge = {
            "first_name": p.first_name,
            "last_name": p.last_name,
            "category": p.category.value,
            "meals": p.meals or "",
            "mealsclass": "badge_{}".format(p.meals or "NO"),
            "photourl": f"/api/v1/participant/photo/{p.id}",
            "positionclass": "badge{0}{1}".format(cix, rix),
            "ix": ix,
        }
        # log.info(f"badge: {badge}")
        badges.append(badge)
        j += 1
        if j == 8:
            j = 0
            pages.append(badges)
            badges = []
    if j > 0:
        pages.append(badges)
    tmpl = tmpl_env.get_template("printbadge.j2")
    return tmpl.render({"pages": pages})


async def generate_namecards(cat: str, ids: str = ""):
    """
    get the Namecards for the bjk by categorie or by ids
    ids: comma separated ids
    """
    if cat:
        prts = await get_participants({"category": cat, "enabled": True})
    else:
        prts = await get_participants({"idbel": {"$in": ids.split(",")}})
    logger.info(f"nr of participants {len(prts)}")
    pages = []
    cards = []
    j = 0
    sorteddocs = sorted(prts, key=lambda x: f"{x.last_name}, {x.first_name}")
    for ix, p in enumerate(sorteddocs):
        rix = j % 2 + 1
        ct = ""
        # ct = p.chesstitle + " " if p.chesstitle else ""
        card = {
            "fullname": "{0}{1} {2}".format(ct, p.last_name, p.first_name),
            "natrating": p.ratingbel or 0,
            "fiderating": p.ratingfide or 0,
            "category": p.category.value,
            "nationalityfide": p.nationalityfide,
            # 'photourl': '/photo/{0}'.format(p.id),
            "positionclass": "card_1{0}".format(rix),
            "ix": ix,
        }
        cards.append(card)
        j += 1
        if j == 2:
            j = 0
            pages.append(cards)
            cards = []
    if j > 0:
        pages.append(cards)
    tmpl = tmpl_env.get_template("printnamecard.j2")
    return tmpl.render({"pages": pages})


async def get_photo(id: str) -> Response:
    photo = await DbParticipant.find_single(
        {
            "id": id,
            "_fieldlist": ["badgeimage", "badgemimetype"],
        }
    )
    return Response(content=photo["badgeimage"], media_type=photo["badgemimetype"])


async def get_photo_bel(idbel: str) -> Response:
    photo = await DbParticipant.find_single(
        {
            "idbel": idbel,
            "_fieldlist": ["badgeimage", "badgemimetype"],
        }
    )
    return Response(content=photo["badgeimage"], media_type=photo["badgemimetype"])


async def upload_photo(id: str, photo: str) -> None:
    try:
        header, data = photo.split(",")
        imagedata = a2b_base64(data)
        su = ParticipantUpdate(
            badgemimetype=header.split(":")[1].split(";")[0],
            badgeimage=imagedata,
            badgelength=len(cast(str, imagedata)),
        )
    except Exception:
        raise RdBadRequest(description="BadPhotoData")
    await update_participant(id, su)


prizetable = {
    "U8": [
        (28047, 1, 82 + 20),
        (32122, 2, 72),
        (30030, 3, 61),
        (28033, 4, 51 + 20),
        (26455, 5, 41),
        (27687, 6, 30),
        (29072, 7, 20),
    ],
    "U10": [
        (25302, 1, 82 + 20),
        (26020, 2, 78),
        (26415, 3, 73),
        (28981, 4, 69),
        (29132, 5, 64),
        (28025, 6, 60),
        (27699, 7, 55),
        (29711, 8, 51),
        (32214, 9, 47),
        (27639, 10, 42 + 20),
        (30242, 11, 38),
        (32453, 12, 33),
        (26656, 13, 29),
        (27883, 14, 24),
        (27214, 15, 20),
    ],
    "U12": [
        (23905, 1, 82 + 20),
        (24556, 2, 78),
        (28075, 3, 74),
        (23564, 4, 70),
        (31809, 5, 67 + 20),
        (26420, 6, 63),
        (26047, 7, 59),
        (26459, 8, 55),
        (27254, 9, 51),
        (24114, 10, 47),
        (24940, 11, 43),
        (28412, 12, 39),
        (30039, 13, 36),
        (20029, 14, 32),
        (22100, 15, 28),
        (23758, 16, 24),
        (25393, 17, 20),
    ],
    "U14": [
        (22648, 1, 82 + 20),
        (19469, 2, 79),
        (19678, 3, 75),
        (27199, 4, 72),
        (22388, 5, 68),
        (23637, 6, 65),
        (23435, 7, 61),
        (23871, 8, 58),
        (22843, 9, 54),
        (30137, 10, 51),
        (22776, 11, 48),
        (25341, 12, 44),
        (25401, 13, 41),
        (23003, 14, 37),
        (21853, 15, 34),
        (27541, 16, 30),
        (19937, 17, 27),
        (20487, 18, 23 + 20),
        (26885, 19, 20),
    ],
    "U16": [
        (22370, 1, 82 + 20),
        (23286, 2, 78),
        (31838, 3, 74),
        (21498, 4, 70),
        (22884, 5, 67),
        (22695, 6, 63),
        (22643, 7, 59),
        (17012, 8, 55),
        (21205, 9, 51),
        (19024, 10, 47),
        (20509, 11, 43),
        (23528, 12, 39),
        (17289, 13, 36),
        (23102, 14, 32),
        (30116, 15, 28),
        (19738, 16, 24),
        (26472, 17, 20),
    ],
    "U18": [
        (20540, 1, 82 + 20),
        (20531, 2, 77),
        (20412, 3, 72),
        (16824, 4, 68),
        (17780, 5, 63),
        (16911, 6, 58),
        (23285, 7, 53),
        (19360, 8, 49),
        (20846, 9, 44),
        (27538, 10, 39),
        (16017, 11, 34),
        (22694, 12, 30),
        (24868, 13, 25),
        (19723, 14, 20),
        (15454, 19, 20),  # 1st girl
    ],
    "U20": [
        (14086, 1, 82 + 20),
        (14606, 2, 70),
        (25749, 3, 57),
        (14603, 4, 45),
        (19700, 5, 32),
        (16881, 6, 20 + 20),
    ],
}


async def generate_prizes(cat: str):
    """
    get the prizes for the bjk by categorie
    """
    from bycco.paymentrequest.paymentrequest import getPaymessage

    pages = []
    cards = []
    j = 0
    for pr in prizetable[cat]:
        pls = await get_participants({"idbel": str(pr[0])})
        pl = pls[0]
        rix = j % 3 + 1
        code = 2025 * 100000 + pr[0]
        card = {
            "name": "{0}, {1}".format(pl.last_name, pl.first_name),
            "category": cat,
            "positionclass": "prize_1{0}".format(rix),
            "place": pr[1],
            "prize": pr[2],
            "code": getPaymessage(code),
        }
        cards.append(card)
        j += 1
        if j == 3:
            j = 0
            pages.append(cards)
            cards = []
    if j > 0:
        pages.append(cards)
    tmpl = tmpl_env.get_template("printprize.j2")
    return tmpl.render({"pages": pages})


async def xls_participant() -> bytes:
    """
    get all registrations in xls format
    """
    docs = await DbParticipant.find_multiple({"_model": Participant})
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Participants"
    ws.append(
        [
            "id",
            "idbel",
            "idfide",
            "idclub",
            "first_name",
            "last_name",
            "category",
            "enabled",
            "emails",
            "locale",
            "nationalityfide",
            "ratingbel",
            "ratingfide",
            "remarks",
            "natstatus",
        ]
    )
    for d in docs:
        ws.append(
            [
                d.id,
                d.idbel,
                d.idfide,
                d.idclub,
                d.first_name,
                d.last_name,
                d.category.value,
                d.enabled,
                ",".join(d.emails),
                d.locale,
                d.nationalityfide,
                d.ratingbel,
                d.ratingfide,
                d.remarks,
                d.natstatus.value,
            ]
        )
    with NamedTemporaryFile() as tmp:
        wb.save(tmp.name)
        tmp.seek(0)
        xlscontent = tmp.read()
    logger.info(f"xlscontent {len(xlscontent)}")
    return xlscontent
