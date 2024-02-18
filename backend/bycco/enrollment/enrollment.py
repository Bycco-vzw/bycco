# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, Optional, List
from datetime import date, datetime, timezone, timedelta
from fastapi import BackgroundTasks
from fastapi.responses import Response
from binascii import a2b_base64

from reddevil.core import get_settings, RdBadRequest, RdNotFound

from bycco.enrollment.md_enrollment import (
    DbEnrollment,
    Enrollment,
    EnrollmentIn,
    EnrollmentUpdate,
    EnrollmentVkIn,
    IdReply,
    NatStatus,
)
from bycco.core.mail import MailParams, sendemail_enrollment_vk
from httpx import (
    TransportError,
    DecodingError,
    AsyncClient,
)


logger = logging.getLogger(__name__)

api_lookupbel = "/api/v1/member/anon/member/{id}"
api_lookupfide = "/api/v1/member/anon/fidemember/{id}"
api_fideis2belid = "/api/v1/member/anon/fideid2belid/{id}"

# crud operations


async def add_enrollment(edict: dict) -> str:
    """
    add an enrollment
    """
    id = await DbEnrollment.add(edict)
    return id


async def update_enrollment(id, eu: EnrollmentUpdate, options: dict = {}) -> Enrollment:
    """
    update a member
    """
    filter = options.copy()
    filter["_model"] = filter.pop("_model", Enrollment)
    mo = cast(
        Enrollment,
        await DbEnrollment.update(id, eu, filter),
    )
    return mo


async def create_enrollment_vk(ei: EnrollmentVkIn) -> str:
    logger.info(f"create an enrollment for VK {ei}")

    if ei.idsub:
        eu = EnrollmentUpdate(
            category=ei.category,
            emailplayer=ei.emailplayer,
            idbel=ei.idbel,
            idfide=ei.idfide,
            locale=ei.locale,
            mobileplayer=ei.mobileplayer,
        )
        enrid = (await update_enrollment(ei.idsub, eu.model_dump(exclude_none=True))).id
    else:
        eidict = ei.model_dump()
        eidict.pop("idsub", None)
        enrid = await add_enrollment(eidict)
    meu = EnrollmentUpdate()
    if ei.idbel:
        try:
            pl = await lookup_idbel(ei.idbel)
            meu.birthyear = pl.birthyear
            meu.gender = pl.gender
            meu.first_name = pl.first_name
            meu.idclub = pl.idclub
            meu.last_name = pl.last_name
            meu.nationalitybel = pl.nationalitybel
            meu.natstatus = pl.natstatus
            meu.ratingbel = pl.ratingbel
        except Exception as e:
            logger.info(f"lookup idbel failed {e}")
    if ei.idfide:
        try:
            pl = await lookup_idfide(ei.idfide)
            meu.birthyear = pl.birthyear
            meu.gender = pl.gender
            meu.first_name = pl.first_name
            meu.last_name = pl.last_name
            meu.nationalityfide = pl.nationalityfide
            meu.natstatus = pl.natstatus
            meu.ratingfide = pl.ratingfide
        except Exception as e:
            logger.info(f"lookup idfide failed {e}")
    await update_enrollment(enrid, meu.model_dump(exclude_none=True))
    return enrid


async def lookup_idbel(idbel: str) -> IdReply:
    """
    lookup member by idbel in KBSB member directory
    """
    settings = get_settings()
    url = api_lookupbel.format(id=idbel)
    try:
        async with AsyncClient() as client:
            rc = await client.get(f"{settings.KBSB_HOST}{url}")
            plyr = rc.json()
    except DecodingError:
        logger.error(f"decoding error on {url}")
        raise RdBadRequest("DecodingErrorKBSB")
    except TransportError:
        logger.error(f"Request error to {url}")
        raise RdBadRequest("RequestErrorKBSB")
    if rc.status_code != 200:
        logger.info(f"failed api call to kbsb lookup_idbel {rc}")
        raise RdNotFound(description="FailedApiKBSB")
    logger.info(f"member by idbel {plyr}")
    return IdReply(
        belfound=True,
        birthyear=plyr["birthyear"],
        first_name=plyr["first_name"],
        gender=plyr["gender"],
        idbel=idbel,
        idclub=str(plyr["idclub"] or 0),
        idfide=str(plyr["idfide"] or 0),
        last_name=plyr["last_name"],
        nationalitybel=plyr["nationalitybel"],
        nationalityfide=plyr["nationalityfide"],
        natstatus=NatStatus.unknown,
        ratingbel=plyr["natrating"],
        ratingfide=plyr["fiderating"],
        subconfirmed=False,
        subid=None,
    )


async def lookup_idfide(idfide: str) -> IdReply:
    settings = get_settings()
    # first see if we have a bel id for the
    url = api_fideis2belid.format(id=idfide)
    try:
        async with AsyncClient() as client:
            rc = await client.get(f"{settings.KBSB_HOST}{url}")
            logger.info(f"reply fide2bel {rc.text}")
    except DecodingError:
        logger.error(f"decoding error on {url}")
        raise RdBadRequest("DecodingErrorKBSB")
    except TransportError:
        logger.error(f"Request error to {url}")
        raise RdBadRequest("RequestErrorKBSB")
    if rc.status_code == 200 and rc.text and rc.text != "0":
        idbel = rc.text
        logger.info(f"redirecting to lookup idbel {idbel}")
        return await lookup_idbel(idbel)
    url = api_lookupfide.format(id=idfide)
    logger.info(f"fetching member by fideid {url}")
    try:
        async with AsyncClient() as client:
            rc = await client.get(f"{settings.KBSB_HOST}{url}")
            plyr = rc.json()
    except DecodingError:
        logger.error(f"decoding error on {url}")
        raise RdBadRequest("DecodingErrorKBSB")
    except TransportError:
        logger.error(f"Request error to {url}")
        raise RdBadRequest("RequestErrorKBSB")
    if rc.status_code != 200:
        logger.info(f"failed api call to kbsb lookup_idfide {rc}")
        raise RdNotFound(description="FailedApiKBSB")
    logger.info(f"plyr {plyr}")
    reply = IdReply(
        belfound=False,
        birthyear=plyr["birthyear"],
        first_name=plyr["first_name"],
        gender=plyr["gender"],
        idbel="",
        idclub="",
        idfide=idfide,
        last_name=plyr["last_name"],
        nationalitybel="",
        nationalityfide=plyr["nationalityfide"],
        natstatus=NatStatus.unknown,
        ratingbel=0,
        ratingfide=plyr["fiderating"],
        subconfirmed=False,
        subid=None,
    )
    return reply


async def upload_photo(id: str, photo: str) -> None:
    try:
        header, data = photo.split(",")
        imagedata = a2b_base64(data)
        su = EnrollmentUpdate(
            badgemimetype=header.split(":")[1].split(";")[0],
            badgeimage=imagedata,
            badgelength=len(cast(str, imagedata)),
        )
    except:
        raise RdBadRequest(description="BadPhotoData")
    await update_enrollment(id, su.model_dump(exclude_none=True))


async def confirm_enrollment_vk(id: str, bt: BackgroundTasks) -> None:
    su = EnrollmentUpdate(confirmed=True, registrationtime=datetime.now(), enabled=True)
    enr = await update_enrollment(id, su.model_dump(exclude_none=True))
    sendemail_enrollment_vk(enr)


async def get_photo(id: str):
    photo = await DbEnrollment.find_single(
        {
            "id": id,
            "_fieldlist": ["badgeimage", "badgemimetype"],
        }
    )
    return Response(content=photo["badgeimage"], media_type=photo["badgemimetype"])
