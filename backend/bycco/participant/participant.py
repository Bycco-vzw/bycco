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
    DbParticpantBJK,
    ParticipantVKCategory,
    ParticipantVKDetail,
    ParticipantVKItem,
    DbParticpantVK,
    Gender,
)
from bycco.enrollment import (
    Enrollment,
    get_enrollment,
    get_enrollments_vk,
    get_enrollments_bjk,
)

from reddevil.core import RdNotFound


async def get_participants_vk(options: dict = {}) -> List[ParticipantVKItem]:
    filter = options.copy()
    filter["_model"] = filter.pop("_model", ParticipantVKItem)
    return [
        cast(ParticipantVKItem, x) for x in await DbParticpantVK.find_multiple(filter)
    ]


async def mgmt_get_participant_vk(id: str) -> ParticipantVKDetail:
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
    enr = cast(Enrollment, await get_enrollment(idenr))
    return await DbParticpantVK.add(
        {
            "badgeimage": enr.badgeimage,
            "badgemimetype": enr.badgemimetype,
            "badgelength": enr.badgelength,
            "birthyear": enr.birthyear,
            "category": ParticipantVKCategory(enr.category.value),
            "chesstitle": enr.chesstitle or "",
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


async def mgmt_import_enrollments_vk():
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
    # now process the idfides withoit idbel
    for idfide, enr in idfides.items():
        if enr.idbel:
            continue
        try:
            par = await get_participant_vk_by_idfide(idfide)
        except RdNotFound:
            par = None
        if par is None:
            await import_participant_vk(enr.id)


async def get_participants_bjk(options: dict = {}) -> List[ParticipantBJKItem]:
    filter = options.copy()
    filter["_model"] = filter.pop("_model", ParticipantBJKItem)
    return [
        cast(ParticipantBJKItem, x) for x in await DbParticpantBJK.find_multiple(filter)
    ]


async def mgmt_get_participant_bjk(id: str) -> ParticipantBJKDetail:
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
    enr = cast(Enrollment, await get_enrollment(idenr))
    return await DbParticpantBJK.add(
        {
            "badgeimage": enr.badgeimage,
            "badgemimetype": enr.badgemimetype,
            "badgelength": enr.badgelength,
            "birthyear": enr.birthyear,
            "category": ParticipantBJKCategory(enr.category.value),
            "chesstitle": enr.chesstitle or "",
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
            "natstatus": enr.natstatus,
            "present": None,
            "ratingbel": enr.ratingbel or 0,
            "ratingfide": enr.ratingfide or 0,
            "remarks": "",
        }
    )


async def mgmt_import_enrollments_bjk():
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
