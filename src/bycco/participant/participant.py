# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, List
from binascii import a2b_base64
from fastapi import Response
from jinja2 import PackageLoader, Environment

from reddevil.core import RdBadRequest, RdNotFound

from bycco.participant import (
    ParticipantBJKCategory,
    ParticipantBJKDetail,
    ParticipantBJKItem,
    ParticipantBJKUpdate,
    ParticipantBJK,
    DbParticpantBJK,
    Gender,
)
from bycco.registration import (
    Registration,
    get_registration_bjk,
    # get_registration_vk,
    get_registrations_bjk,
    # get_registrations_vk,
    lookup_idbel,
    lookup_idfide,
)

logger = logging.getLogger(__name__)
tmpl_env = Environment(loader=PackageLoader("bycco"), trim_blocks=True)
# bjk


async def get_participants_bjk(options: dict | None = None) -> List[ParticipantBJKItem]:
    filter = options.copy() if options else {}
    filter["_model"] = filter.pop("_model", ParticipantBJKItem)
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["_fieldlist"].append("_creationtime")
    logger.info(f"get_participants_bjk {filter}")
    return [
        cast(ParticipantBJKItem, x) for x in await DbParticpantBJK.find_multiple(filter)
    ]


async def get_participant_bjk(id: str) -> ParticipantBJKDetail:
    filter = {"_model": ParticipantBJKDetail}
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["_fieldlist"].append("_creationtime")
    filter["id"] = id
    par = await DbParticpantBJK.find_single(filter)
    return par


async def get_participant_bjk_by_idbel(idbel: str) -> ParticipantBJKItem:
    filter = {"_model": ParticipantBJKItem}
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["idbel"] = idbel
    return await DbParticpantBJK.find_single(filter)


async def create_participant_bjk(idbel: str, category: ParticipantBJKCategory) -> None:
    """
    create a participant
    """
    pl = await lookup_idbel(idbel)
    return await DbParticpantBJK.add(
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


async def import_participant_bjk(idreg) -> str:
    """
    import an enrollemnt and create a participant
    return the id of the participant
    """
    enr = cast(
        Registration, await get_registration_bjk(idreg, {"_model": Registration})
    )
    return await DbParticpantBJK.add(
        {
            "badgeimage": enr.badgeimage,
            "badgemimetype": enr.badgemimetype,
            "badgelength": enr.badgelength,
            "birthyear": enr.birthyear,
            "category": ParticipantBJKCategory(enr.category.value),
            "chesstitle": enr.chesstitle or "",
            "enabled": True,
            "emails": enr.emailplayer.split(",")
            + enr.representative.emailparent.split(",")
            + enr.representative.emailattendant.split(","),
            "first_name": enr.first_name,
            "gender": Gender(enr.gender) if enr.gender else None,
            "idbel": enr.idbel,
            "idclub": enr.idclub,
            "idfide": enr.idfide,
            "locale": enr.locale,
            "last_name": enr.last_name,
            "nationalityfide": enr.nationalityfide,
            "natstatus": enr.natstatus,
            "present": None,
            "ratingbel": enr.ratingbel or 0,
            "ratingfide": enr.ratingfide or 0,
            "remarks": "",
        }
    )


async def import_participants_bjk():
    """
    import all registration for the bjk 2025
    check doubles5
    retain most recent registration for the same person
    """
    enrs = await get_registrations_bjk({"confirmed": True})
    idbels = {}
    for enr in enrs:
        if enr.idbel in idbels:
            # we have a double detected via idbel
            if enr.registrationtime > idbels[enr.idbel].registrationtime:
                idbels[enr.idbel] = enr
        else:
            idbels[enr.idbel] = enr
    # process the participants
    for idbel, enr in idbels.items():
        try:
            par = await get_participant_bjk_by_idbel(idbel)
        except RdNotFound:
            par = None
        if par is None:
            await import_participant_bjk(enr.id)


async def update_participant_bjk(
    id: str, par: ParticipantBJKUpdate, options: dict = {}
) -> ParticipantBJK:
    opt = options.copy()
    opt["_model"] = opt.pop("_model", ParticipantBJKDetail)
    upd = par.model_dump(exclude_unset=True)
    return cast(
        ParticipantBJK,
        await DbParticpantBJK.update(id, upd, opt),
    )


async def update_elo_bjk() -> None:
    """
    update the elo of all participants
    """
    prts = await get_participants_bjk()
    for pr in prts:
        if not pr.enabled:
            continue
        logger.info(f"updating elo {pr.last_name} {pr.first_name}")
        upd = ParticipantBJK()
        if pr.idbel and pr.idbel != "0":
            try:
                pl = await lookup_idbel(pr.idbel)
                upd.ratingbel = pl.ratingbel
            except Exception:
                logger.info(f"lookup idbel failed {pr.last_name} {pr.first_name}")
        if pr.idfide and pr.idfide != "0":
            try:
                pl = await lookup_idfide(pr.idfide)
                upd.ratingfide = pl.ratingfide
            except Exception:
                logger.info(f"lookup idfide failed {pr.last_name} {pr.first_name}")
        if upd:
            await update_participant_bjk(pr.id, upd)


async def generate_badges_bjk(cat: str, ids: str = ""):
    """
    get the Namecards for the bjk by categorie or by ids
    cat: str
    ids: comma separated ids
    """
    logger.info(f"generate_badges_bjk cat={cat} ids={ids}")
    if cat:
        prts = await get_participants_bjk({"category": cat, "enabled": True})
    else:
        prts = await get_participants_bjk(
            {"idbel": {"$in": ids.split(",")}, "enabled": True}
        )
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
    tmpl = tmpl_env.get_template("printbadge_bjk.j2")
    return tmpl.render({"pages": pages})


async def generate_namecards_bjk(cat: str, ids: str = ""):
    """
    get the Namecards for the bjk by categorie or by ids
    ids: comma separated ids
    """
    if cat:
        prts = await get_participants_bjk({"category": cat, "enabled": True})
    else:
        prts = await get_participants_bjk({"idbel": {"$in": ids.split(",")}})
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
    tmpl = tmpl_env.get_template("printnamecard_bjk.j2")
    return tmpl.render({"pages": pages})


async def get_photo(id: str) -> Response:
    photo = await DbParticpantBJK.find_single(
        {
            "id": id,
            "_fieldlist": ["badgeimage", "badgemimetype"],
        }
    )
    return Response(content=photo["badgeimage"], media_type=photo["badgemimetype"])


async def get_photo_bel(idbel: str) -> Response:
    photo = await DbParticpantBJK.find_single(
        {
            "idbel": idbel,
            "_fieldlist": ["badgeimage", "badgemimetype"],
        }
    )
    return Response(content=photo["badgeimage"], media_type=photo["badgemimetype"])


async def upload_photo_bjk(id: str, photo: str) -> None:
    try:
        header, data = photo.split(",")
        imagedata = a2b_base64(data)
        su = ParticipantBJKUpdate(
            badgemimetype=header.split(":")[1].split(";")[0],
            badgeimage=imagedata,
            badgelength=len(cast(str, imagedata)),
        )
    except Exception:
        raise RdBadRequest(description="BadPhotoData")
    await update_participant_bjk(id, su)


prizetable = {
    "U8": [
        (26415, 1, 75 + 20),
        (26020, 2, 65),
        (28047, 3, 55),
        (27883, 4, 45 + 20),
        (26868, 5, 35),
        (30561, 6, 25),
        (30176, 7, 15),
    ],
    "U10": [
        (23905, 1, 75 + 20),
        (25302, 2, 70),
        (24940, 3, 65),
        (24114, 4, 60),
        (25179, 5, 55),
        (26776, 6, 50),
        (26912, 7, 45),
        (26656, 8, 40),
        (25558, 9, 35),
        (30039, 10, 30),
        (28366, 11, 25 + 20),
        (25549, 12, 20),
        (21389, 13, 15),
    ],
    "U12": [
        (22648, 1, 75 + 20),
        (27030, 2, 71),
        (22843, 3, 67),
        (21853, 4, 63),
        (23564, 5, 59),
        (24556, 6, 55),
        (21597, 7, 51),
        (19937, 8, 47),
        (30069, 9, 43),
        (22100, 10, 39),
        (22448, 11, 35 + 20),
        (23901, 12, 31),
        (26877, 13, 27),
        (20029, 14, 23),
        (26885, 15, 19),
        (28075, 16, 15),
    ],
    "U14": [
        (21132, 1, 75 + 20),
        (22643, 2, 71),
        (23003, 3, 66),
        (19678, 4, 62),
        (23871, 5, 58),
        (20487, 6, 54 + 20),
        (22388, 7, 49),
        (27199, 8, 45),
        (22027, 9, 41),
        (24009, 10, 36),
        (23102, 11, 32),
        (19738, 12, 28),
        (21109, 13, 24),
        (20498, 14, 19),
        (25839, 15, 15),
    ],
    "U16": [
        (20531, 1, 75 + 20),
        (20540, 2, 71),
        (22370, 3, 67),
        (23285, 4, 63),
        (17780, 5, 59),
        (16017, 6, 55),
        (17669, 7, 51),
        (19360, 8, 47),
        (25611, 9, 43),
        (16824, 10, 39),
        (17012, 11, 35),
        (17289, 12, 31),
        (22695, 13, 27 + 20),
        (27160, 14, 23),
        (23150, 15, 19),
        (21498, 16, 15),
    ],
    "U18": [
        (14086, 1, 75 + 20),
        (16911, 2, 71),
        (14606, 3, 67),
        (25749, 4, 63),
        (22694, 5, 59),
        (18802, 6, 55),
        (16881, 7, 51 + 20),
        (18195, 8, 47),
        (14577, 9, 43),
        (28856, 10, 39),
        (28350, 11, 35),
        (26470, 12, 31),
        (21117, 13, 27),
        (27869, 14, 23),
        (23247, 15, 19),
        (22957, 16, 15),
    ],
    "U20": [
        (17648, 1, 75 + 20),
        (12445, 2, 55),
        (14078, 3, 35),
        (14603, 4, 15),
        (14625, 5, 20),
    ],
}


async def generate_prizes_bjk(cat: str):
    """
    get the prizes for the bjk by categorie
    """
    from bycco.paymentrequest.paymentrequest import getPaymessage

    pages = []
    cards = []
    j = 0
    for pr in prizetable[cat]:
        pls = await get_participants_bjk({"idbel": str(pr[0])})
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
    tmpl = tmpl_env.get_template("printprize_bjk.j2")
    return tmpl.render({"pages": pages})
