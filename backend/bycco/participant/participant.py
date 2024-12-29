# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, List, Dict, Any
from datetime import datetime
from binascii import a2b_base64
from fastapi import BackgroundTasks, Response
from jinja2 import FileSystemLoader, Environment

from reddevil.core import get_settings, RdBadRequest, RdNotFound

from bycco.participant import (
    ParticipantBJKCategory,
    ParticipantBJKDetail,
    ParticipantBJKItem,
    ParticipantBJKUpdate,
    ParticipantBJKDB,
    ParticipantBJK,
    DbParticpantBJK,
    # ParticipantVKCategory,
    # ParticipantVKDetail,
    # ParticipantVKItem,
    # ParticipantVK,
    # DbParticpantVK,
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

from reddevil.core import RdNotFound

logger = logging.getLogger(__name__)
env = Environment(loader=FileSystemLoader("bycco/templates"), trim_blocks=True)

# bjk


async def get_participants_bjk(options: dict = {}) -> List[ParticipantBJKItem]:
    filter = options.copy()
    filter["_model"] = filter.pop("_model", ParticipantBJKItem)
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["_fieldlist"].append("_creationtime")
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
            except Exception as e:
                logger.info(f"lookup idbel failed {pr.last_name} {pr.first_name}")
        if pr.idfide and pr.idfide != "0":
            try:
                pl = await lookup_idfide(pr.idfide)
                upd.ratingfide = pl.ratingfide
            except Exception as e:
                logger.info(f"lookup idfide failed {pr.last_name} {pr.first_name}")
        if upd:
            await update_participant_bjk(pr.id, upd)


async def generate_badges_bjk(cat: str, ids: str = ""):
    """
    get the Namecards for the bjk by categorie or by ids
    cat: str
    ids: comma separated ids
    """
    filter: Dict[str, Any] = {"enabled": True}
    if cat:
        prts = await get_participants_bjk({"category": cat})
    else:
        prts = await get_participants_bjk({"idbel": {"$in": ids.split(",")}})
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
            # "meals": p.meals or "",
            # "mealsclass": "badge_{}".format(p.meals or "NO"),
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
    tmpl = env.get_template("printbadge_bjk.j2")
    return tmpl.render({"pages": pages})


async def generate_namecards_bjk(cat: str, ids: str = ""):
    """
    get the Namecards for the bjk by categorie or by ids
    ids: comma separated ids
    """
    filter: Dict[str, Any] = {"enabled": True}
    if cat:
        prts = await get_participants_bjk({"category": cat})
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
    tmpl = env.get_template("printnamecard_bjk.j2")
    return tmpl.render({"pages": pages})


async def get_photo(id: str) -> Response:
    photo = await DbParticpantBJK.find_single(
        {
            "id": id,
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
    except:
        raise RdBadRequest(description="BadPhotoData")
    await update_participant_bjk(id, su)


prizetable = {
    "U8": [
        (25302, 1, 80 + 20),
        (26415, 2, 70),
        (28025, 3, 60),
        (26020, 4, 50),
        (26912, 5, 40),
        (28047, 6, 30),
        (26656, 7, 20),
        (27639, 10, 0 + 20),
    ],
    "U10": [
        (23905, 1, 80 + 20),
        (22100, 2, 73),
        (24556, 3, 67),
        (24940, 4, 60),
        (23909, 5, 53),
        (23564, 6, 47),
        (23466, 7, 40),
        (23668, 8, 33),
        (24114, 9, 27),
        (26502, 10, 20 + 20),
    ],
    "U12": [
        (22648, 1, 80 + 20),
        (23637, 2, 76),
        (19469, 3, 71),
        (19937, 4, 67),
        (22843, 5, 63),
        (22388, 6, 59),
        (22027, 7, 54),
        (20487, 8, 50 + 20),
        (20829, 9, 46),
        (23901, 10, 41),
        (19678, 11, 37),
        (23435, 12, 33),
        (22025, 13, 29),
        (21597, 14, 24),
        (24637, 15, 20),
    ],
    "U14": [
        (21132, 1, 80 + 20),
        (22370, 2, 75),
        (21205, 3, 71),
        (19024, 4, 66),
        (22643, 5, 62),
        (23528, 6, 57),
        (22695, 7, 52 + 20),
        (17012, 8, 48),
        (20065, 9, 43),
        (17289, 10, 38),
        (19738, 11, 34),
        (23102, 12, 29),
        (19230, 13, 25),
        (22007, 14, 20),
    ],
    "U16": [
        (20531, 1, 80 + 20),
        (20540, 2, 76),
        (16017, 3, 72),
        (20846, 4, 68),
        (17684, 5, 64),
        (16911, 6, 60),
        (22966, 7, 56),
        (16824, 8, 52),
        (23285, 9, 48),
        (19109, 10, 44),
        (23150, 11, 40),
        (23247, 12, 36),
        (19723, 13, 32),
        (21117, 14, 28 + 20),
        (15465, 15, 24),
        (22694, 16, 20),
    ],
    "U18": [
        (14606, 1, 80 + 20),
        (14724, 2, 73),
        (25749, 3, 65),
        (15064, 4, 58),
        (26095, 5, 50),
        (18195, 6, 43),
        (14898, 7, 35),
        (15721, 8, 28),
        (20817, 9, 20),
        (14639, 15, 0 + 20),
    ],
    "U20": [
        (12445, 1, 80 + 20),
        (14450, 2, 65),
        (19430, 3, 50),
        (12007, 4, 35),
        (17648, 5, 20),
        (14625, 6, 0 + 20),
    ],
}


async def generate_prizes_bjk():
    """
    get the prizes for the bjk by categorie
    """
    from bycco.paymentrequest.paymentrequest import getPaymessage

    pages = []
    cards = []
    j = 0
    for cat in ["U8", "U10", "U12", "U14", "U16", "U18", "U20"]:
        for pr in prizetable[cat]:
            pls = await get_participants_bjk({"idbel": str(pr[0])})
            pl = pls[0]
            rix = j % 3 + 1
            code = 2024 * 100000 + pr[0]
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
    tmpl = env.get_template("printprize_bjk.j2")
    return tmpl.render({"pages": pages})
