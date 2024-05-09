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
    ParticipantVKCategory,
    ParticipantVKDetail,
    ParticipantVKItem,
    ParticipantVK,
    DbParticpantVK,
    DbParticpantBJK,
    Gender,
)
from bycco.enrollment import (
    Enrollment,
    get_enrollment_bjk,
    get_enrollment_vk,
    get_enrollments_bjk,
    get_enrollments_vk,
    lookup_idbel,
    lookup_idfide,
)

from reddevil.core import RdNotFound

logger = logging.getLogger(__name__)
env = Environment(loader=FileSystemLoader("bycco/templates"), trim_blocks=True)

# vk


async def get_participants_vk(options: dict = {}) -> List[ParticipantVKItem]:
    filter = options.copy()
    filter["_model"] = filter.pop("_model", ParticipantVKItem)
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    return [
        cast(ParticipantVKItem, x) for x in await DbParticpantVK.find_multiple(filter)
    ]


async def get_participant_vk(id: str) -> ParticipantVKDetail:
    filter = {"_model": ParticipantVKDetail}
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["id"] = id
    return await DbParticpantVK.find_single(filter)


async def get_participant_vk_by_idbel(idbel: str) -> ParticipantVKItem:
    filter = {"_model": ParticipantVKItem}
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["idbel"] = idbel
    return await DbParticpantVK.find_single(filter)


async def get_participant_vk_by_idfide(idfide: str) -> ParticipantVKItem:
    filter = {"_model": ParticipantVKItem}
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["idfide"] = idfide
    return await DbParticpantVK.find_single(filter)


async def import_participant_vk(idenr) -> str:
    """
    import an enrollemnt and create a participant
    return the id of the participant
    """
    enr = cast(Enrollment, await get_enrollment_vk(idenr))
    # solving transitional issue with chesstitle
    chesstitle = enr.chesstitle or ""
    return await DbParticpantVK.add(
        {
            "badgeimage": enr.badgeimage,
            "badgemimetype": enr.badgemimetype,
            "badgelength": enr.badgelength,
            "birthyear": enr.birthyear,
            "category": ParticipantVKCategory(enr.category.value),
            "chesstitle": chesstitle,
            "enabled": True,
            "emails": enr.emailplayer.split(","),
            "first_name": enr.first_name,
            "gender": Gender(enr.gender),
            "idbel": enr.idbel,
            "idclub": enr.idclub,
            "idfide": enr.idfide,
            "locale": enr.locale,
            "last_name": enr.last_name,
            "nationalityfide": enr.nationalityfide,
            "present": None,
            "ratingbel": enr.ratingbel or 0,
            "ratingfide": enr.ratingfide or 0,
            "remarks": "",
        }
    )


async def import_participants_vk():
    """
    import all enrollment for the vk 2024
    check doubles
    retain most recent enrollment for the same person
    """
    enrs = await get_enrollments_vk({"confirmed": True})
    idbels = {}
    idfides = {}
    for enr in enrs:
        if enr.idbel and enr.idbel != "0" and enr.idbel in idbels:
            # we have a double detected via idbel
            if enr.registrationtime > idbels[enr.idbel].registrationtime:
                idbels[enr.idbel] = enr
        elif enr.idfide and enr.idfide != "0" and enr.idfide in idfides:
            # we have a double detected via idfide
            if enr.registrationtime > idfides[enr.idfide].registrationtime:
                idfides[enr.idfide] = enr
        else:
            if enr.idbel:
                idbels[enr.idbel] = enr
            if enr.idfide:
                idfides[enr.idfide] = enr
    # first process the participants with an idbel
    for idbel, enr in idbels.items():
        try:
            par = await get_participant_vk_by_idbel(idbel)
        except RdNotFound:
            par = None
        if par is None:
            await import_participant_vk(enr.id)
    # now process the participants with the idfides but without idbel
    for idfide, enr in idfides.items():
        if enr.idbel:
            continue
        try:
            par = await get_participant_vk_by_idfide(idfide)
        except RdNotFound:
            par = None
        if par is None:
            await import_participant_vk(enr.id)


async def update_participant_vk(
    id: str, par: ParticipantVK, options: dict = {}
) -> ParticipantVK:
    opt = options.copy()
    opt["_model"] = opt.pop("_model", ParticipantVK)
    return cast(
        ParticipantVK,
        await DbParticpantVK.update(id, par.model_dump(exclude_unset=True), opt),
    )


async def update_elo_vk() -> None:
    """
    update the elo of all participants
    """
    prts = await get_participants_vk()
    for pr in prts:
        upd = ParticipantVK()
        if pr.idbel:
            try:
                pl = await lookup_idbel(pr.idbel)
                upd.ratingbel = pl.ratingbel
            except Exception as e:
                logger.info(f"lookup idbel failed {e}")
        if pr.idfide:
            try:
                pl = await lookup_idfide(pr.idfide)
                upd.ratingfide = pl.ratingfide
            except Exception as e:
                logger.info(f"lookup idfide failed {e}")
        if upd:
            await update_participant_vk(pr.id, upd)


async def generate_namecards_vk(cat: str, ids: str):
    """
    get the Namecards for the vk by categorie or by ids
    ids: comma separated ids
    """
    filter: Dict[str, Any] = {"enabled": True}
    logger.info(f"filter {filter}")
    if cat:
        prts = await get_participants_vk({"category": cat})
    else:
        prts = await get_participants_vk({"idbel": {"$in": ids.split(",")}})
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
    tmpl = env.get_template("printnamecard_vk.j2")
    return tmpl.render({"pages": pages})


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


async def import_participant_bjk(idenr) -> str:
    """
    import an enrollemnt and create a participant
    return the id of the participant
    """
    enr = cast(Enrollment, await get_enrollment_bjk(idenr))
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
            "gender": Gender(enr.gender),
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
    import all enrollment for the bjk 2024
    check doubles
    retain most recent enrollment for the same person
    """
    enrs = await get_enrollments_bjk({"confirmed": True})
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
