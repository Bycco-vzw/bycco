# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, Optional, List
from datetime import date, datetime, timezone, timedelta
from fastapi import BackgroundTasks

from reddevil.core import get_settings, RdBadRequest, RdNotFound

from bycco.enrollment.md_enrollment import (
    EnrollmentVkIn,
    IdReply,
    NatStatus,
)

from httpx import (
    TransportError,
    DecodingError,
    AsyncClient,
)

logger = logging.getLogger(__name__)

api_lookupbel = "/api/v1/member/anon/member/{id}"
api_lookupfide = "/api/v1/member/anon/fidemember/{id}"
api_fideis2belid = "/api/v1/member/anon/fideid2belid/{id}"


async def create_enrollment_vk(enr: EnrollmentVkIn) -> str:
    pass


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
    logger.info(f"member idbel {plyr}")
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
        belfound=True,
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
