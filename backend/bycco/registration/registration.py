# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, Optional, List
from datetime import date, datetime, timezone, timedelta
from fastapi import BackgroundTasks
from fastapi.responses import Response
from binascii import a2b_base64
from httpx import (
    TransportError,
    DecodingError,
    AsyncClient,
)

from reddevil.core import get_settings, RdBadRequest, RdNotFound
from bycco.registration import (
    DbRegistration,
    Registration,
    RegistrationIn,
    RegistrationItem,
    RegistrationNoBadge,
    RegistrationUpdate,
    IdReply,
    NatStatus,
)


logger = logging.getLogger(__name__)

logger.info("loading registration code")

api_lookupbel = "/api/v1/member/anon/member/{id}"
api_lookupfide = "/api/v1/member/anon/fidemember/{id}"
api_fideis2belid = "/api/v1/member/anon/fideid2belid/{id}"

# crud operations


async def add_registration(edict: dict) -> str:
    """
    add an registration
    """
    id = await DbRegistration.add(edict)
    return id


async def get_registrations_bjk(options: dict = {}) -> List[RegistrationItem]:
    """
    get registrations
    """
    filter = options.copy()
    filter["_model"] = filter.pop("_model", RegistrationItem)
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["event"] = "bjk2025"
    return [
        cast(RegistrationItem, x) for x in await DbRegistration.find_multiple(filter)
    ]


async def get_registration_bjk(id: str, options: dict = {}) -> RegistrationNoBadge:
    """
    get registrations
    """
    filter = options.copy()
    filter["_model"] = filter.pop("_model", RegistrationNoBadge)
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["id"] = id
    filter["event"] = "bjk2025"
    reg = cast(RegistrationNoBadge, await DbRegistration.find_single(filter))
    return reg


async def update_registration(
    id: str, eu: RegistrationUpdate, options: dict = {}
) -> Registration:
    """
    update an registration
    """
    filter = options.copy()
    filter["_model"] = filter.pop("_model", Registration)
    eudict = eu.model_dump(exclude_unset=True)
    if "representative" in eudict:
        eudict["representative"] = {
            "emailattendant": eudict.pop("emailattendant", ""),
            "emailparent": eudict.pop("emailparent", ""),
            "fullnameattendant": eudict.pop("fullnameattendant", ""),
            "fullnameparent": eudict.pop("fullnameparent", ""),
            "mobileattendant": eudict.pop("mobileattendant", ""),
            "mobileparent": eudict.pop("mobileparent", ""),
        }
    mo = cast(
        Registration,
        await DbRegistration.update(id, eudict, filter),
    )
    mo.badgeimage = None
    return mo


# business methods


async def create_registration_bjk(ei: RegistrationIn) -> str:
    logger.info(f"create an registration for BJK {ei.idbel} {ei.idfide}")
    if ei.idfide == "0":
        ei.idfide = ""
    if ei.idsub:
        eu = RegistrationUpdate(
            category=ei.category,
            emailattendant=ei.emailattendant,
            emailparent=ei.emailparent,
            emailplayer=ei.emailplayer,
            fullnameattendant=ei.fullnameattendant,
            fullnameparent=ei.fullnameparent,
            idbel=ei.idbel,
            idfide=ei.idfide,
            locale=ei.locale,
            mobileattendant=ei.mobileattendant,
            mobileparent=ei.mobileparent,
            mobileplayer=ei.mobileplayer,
        )
        enrid = (await update_registration(ei.idsub, eu)).id
    else:
        eidict = ei.model_dump()
        eidict.pop("idsub", None)
        eidict["event"] = "bjk2025"
        eidict["representative"] = {
            "emailattendant": eidict.pop("emailattendant", ""),
            "emailparent": eidict.pop("emailparent", ""),
            "fullnameattendant": eidict.pop("fullnameattendant", ""),
            "fullnameparent": eidict.pop("fullnameparent", ""),
            "mobileattendant": eidict.pop("mobileattendant", ""),
            "mobileparent": eidict.pop("mobileparent", ""),
        }
        enrid = await add_registration(eidict)
    meu = RegistrationUpdate()
    try:
        if ei.idfide:
            pl = await lookup_idfide(ei.idfide)
            meu.ratingfide = pl.ratingfide
        else:
            pl = await lookup_idbel(ei.idbel)
            meu.ratingfide = 0
        meu.birthyear = pl.birthyear
        meu.gender = pl.gender
        meu.first_name = pl.first_name
        meu.idclub = pl.idclub
        meu.last_name = pl.last_name
        meu.nationalitybel = pl.nationalitybel
        meu.nationalityfide = pl.nationalityfide
        meu.natstatus = pl.natstatus
        meu.ratingbel = pl.ratingbel
    except Exception as e:
        logger.info(f"lookup idbel failed {e}")
    await update_registration(enrid, meu)
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
        raise RdBadRequest("DecodingErrorKBSB")
    except TransportError:
        raise RdBadRequest("TransportErrorKBSB")
    if rc.status_code != 200:
        logger.info(f"failed api call to kbsb lookup_idbel {rc}")
        raise RdNotFound(description="FailedApiKBSB")
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
            if rc.status_code == 200 and rc.text and rc.text != "0":
                idbel = rc.text
                belreply = await lookup_idbel(idbel)
            else:
                idbel = ""
                belreply = None
    except DecodingError:
        raise RdBadRequest(description="DecodingErrorKBSB")
    except TransportError:
        raise RdBadRequest(description="TransportErrorKBSB")
    url = api_lookupfide.format(id=idfide)
    try:
        async with AsyncClient() as client:
            rc = await client.get(f"{settings.KBSB_HOST}{url}")
            plyr = rc.json()
    except DecodingError:
        raise RdBadRequest("DecodingErrorKBSB")
    except TransportError:
        raise RdBadRequest("TransportErrorKBSB")
    if rc.status_code != 200:
        logger.info(f"failed api call to kbsb lookup_idfide {rc}")
        raise RdNotFound(description="FailedApiKBSB")
    reply = IdReply(
        belfound=belreply is not None,
        birthyear=plyr["birthyear"],
        chesstitle=plyr.get("chesstitle", ""),
        first_name=plyr["first_name"],
        gender=plyr["gender"],
        idbel=idbel,
        idclub="",
        idfide=idfide,
        last_name=plyr["last_name"],
        nationalitybel=belreply.nationalitybel if belreply else "",
        nationalityfide=plyr["nationalityfide"],
        natstatus=NatStatus.unknown,
        ratingbel=belreply.ratingbel if belreply else 0,
        ratingfide=plyr["fiderating"],
        subconfirmed=False,
        subid=None,
    )
    return reply


async def upload_photo(id: str, photo: str) -> None:
    try:
        header, data = photo.split(",")
        imagedata = a2b_base64(data)
        su = RegistrationUpdate(
            badgemimetype=header.split(":")[1].split(";")[0],
            badgeimage=imagedata,
            badgelength=len(cast(str, imagedata)),
        )
    except:
        raise RdBadRequest(description="BadPhotoData")
    await update_registration(id, su)


async def confirm_registration(id: str, bt: BackgroundTasks) -> None:
    su = RegistrationUpdate(
        confirmed=True, registrationtime=datetime.now(), enabled=True
    )
    enr = await update_registration(id, su)
    sendemail_registration_bjk(enr)


async def get_photo(id: str):
    photo = await DbRegistration.find_single(
        {
            "id": id,
            "_fieldlist": ["badgeimage", "badgemimetype"],
        }
    )
    return Response(content=photo["badgeimage"], media_type=photo["badgemimetype"])


def sendemail_registration_bjk(enr: Registration) -> None:
    from bycco.core.mail import MailParams, sendemail_no_attachments

    settings = get_settings()
    em1 = enr.emailplayer.split(",")
    em2 = enr.representative.emailattendant.split(",")
    em3 = enr.representative.emailparent.split(",")
    mp = MailParams(
        subject="BJK 2025 / CBJ 2025 / BJLM 2025",
        sender=settings.EMAIL["sender"],
        receiver=",".join(em1 + em2 + em3),
        template="mailregistration_bjk_{locale}.md",
        locale=enr.locale,
        attachments=[],
        bcc=settings.EMAIL["bcc_registration"],
    )
    edict = enr.model_dump()
    edict["category"] = edict["category"].value
    if enr.nationalityfide:
        edict["natstatus"] = 0 if enr.nationalityfide == "BEL" else 1
    else:
        edict["natstatus"] = 2
    sendemail_no_attachments(mp, edict, "confirmation registration")
