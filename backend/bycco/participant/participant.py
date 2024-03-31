# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, List
from datetime import datetime
from fastapi import BackgroundTasks

from reddevil.core import get_settings, RdBadRequest, RdNotFound
from bycco.core.mail import MailParams, sendemail_no_attachments

from bycco.participant import (
    ParticipantBJKCategory,
    ParticipantBJKDetail,
    ParticipantBJKItem,
    ParticipantBJK,
    DbParticpantBJK,
    ParticipantVKCategory,
    ParticipantVKDetail,
    ParticipantVKItem,
    ParticipantVK,
    DbParticpantVK,
    Gender,
)
from bycco.enrollment import (
    Enrollment,
    get_enrollment_bjk,
    get_enrollment_vk,
    get_enrollments_bjk,
    get_enrollments_vk,
    lookup_idfide,
)

from reddevil.core import RdNotFound

logger = logging.getLogger(__name__)

# vk


async def get_participants_vk(options: dict = {}) -> List[ParticipantVKItem]:
    filter = options.copy()
    filter["_model"] = filter.pop("_model", ParticipantVKItem)
    return [
        cast(ParticipantVKItem, x) for x in await DbParticpantVK.find_multiple(filter)
    ]


async def get_participant_vk(id: str) -> ParticipantVKDetail:
    return await DbParticpantVK.find_single({"_model": ParticipantVKDetail, "id": id})


async def get_participant_vk_by_idbel(idbel: str) -> ParticipantVKItem:
    return await DbParticpantVK.find_single(
        {"_model": ParticipantVKItem, "idbel": idbel}
    )


async def get_participant_vk_by_idfide(idfide: str) -> ParticipantVKItem:
    return await DbParticpantVK.find_single(
        {"_model": ParticipantVKDetail, "idfide": idfide}
    )


async def import_participant_vk(idenr) -> str:
    """
    import an enrollemnt and create a participant
    return the id of the participant
    """
    enr = cast(Enrollment, await get_enrollment_vk(idenr))
    # solving transitional issue with chesstitle
    if enr.idfide and enr.ratingfide and enr.ratingfide > 2100:
        idreply = await lookup_idfide(enr.idfide)
        chesstitle = idreply.chesstitle
    else:
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
        if enr.idbel and enr.idbel in idbels:
            # we have a double detected via idbel
            if enr.registrationtime > idbels[enr.idbel].registrationtime:
                idbels[enr.idbel] = enr
        elif enr.idfide and enr.idfide in idfides:
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


async def update_participate_vk(
    id: str, par: ParticipantVK, options: dict = {}
) -> ParticipantVK:
    opt = options.copy()
    opt["_model"] = opt.pop("_model", ParticipantVK)
    return cast(
        ParticipantVK,
        await DbParticpantVK.update(id, par.model_dump(exclude_unset=True), opt),
    )


# bjk


async def get_participants_bjk(options: dict = {}) -> List[ParticipantBJKItem]:
    filter = options.copy()
    filter["_model"] = filter.pop("_model", ParticipantBJKItem)
    return [
        cast(ParticipantBJKItem, x) for x in await DbParticpantBJK.find_multiple(filter)
    ]


async def get_participant_bjk(id: str) -> ParticipantBJKDetail:
    return await DbParticpantBJK.find_single({"_model": ParticipantBJKDetail, "id": id})


async def get_participant_bjk_by_idbel(idbel: str) -> ParticipantBJKItem:
    return await DbParticpantBJK.find_single(
        {"_model": ParticipantBJKItem, "idbel": idbel}
    )


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
        if enr.first_name == "Kobe":
            logger.info(f"enr {enr}")
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


async def update_participate_bjk(
    id: str, par: ParticipantBJK, options: dict = {}
) -> ParticipantBJK:
    opt = options.copy()
    opt["_model"] = opt.pop("_model", ParticipantBJK)
    return cast(
        ParticipantBJK,
        await DbParticpantBJK.update(id, par.model_dump(exclude_unset=True), opt),
    )


#########
