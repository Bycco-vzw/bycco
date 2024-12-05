# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from typing import List
from fastapi import HTTPException, BackgroundTasks, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema
from reddevil.core import validate_token

router = APIRouter(prefix="/api/v1/registration")

from bycco.registration import (
    RegistrationVkIn,
    Registration,
    RegistrationIn,
    RegistrationItem,
    RegistrationUpdate,
    IdReply,
    confirm_registration,
    create_registration_vk,
    create_registration_bjk,
    get_registration_bjk,
    get_registration_vk,
    get_registrations_bjk,
    get_registrations_vk,
    get_photo,
    lookup_idbel,
    lookup_idfide,
    send_notconfirmed_vk,
    update_registration,
    upload_photo,
)

logger = logging.getLogger(__name__)

# vk


@router.get("/vk", response_model=List[RegistrationItem])
async def api_get_registrations_vk():
    try:
        logger.info("call api get registrations_vk")
        return await get_registrations_vk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_registrations_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/vk/{id}", response_model=Registration)
async def api_get_registrations_vk(id: str):
    try:
        return await get_registration_vk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_registrations_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/vk", response_model=str)
async def api_create_registration_vk(enr: RegistrationVkIn):
    try:
        id = await create_registration_vk(enr)
        return id
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_registration_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/vk/{id}", response_model=Registration)
async def api_update_registration_vk(id: str, enr: RegistrationUpdate):
    try:
        id = await update_registration(id, enr)
        return id
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_registration_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# bjk


@router.get("/bjk", response_model=List[RegistrationItem])
async def api_get_registrations_bjk():
    try:
        return await get_registrations_bjk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_registrations_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/bjk/{id}", response_model=Registration)
async def api_get_registrations_bjk(id: str):
    try:
        return await get_registration_bjk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_registration_bjk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/bjk", response_model=str)
async def api_create_registration_bjk(enr: RegistrationIn):
    try:
        id = await create_registration_bjk(enr)
        return id
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_registration_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/bjk/{id}", response_model=Registration)
async def api_update_registration_vk(id: str, enr: RegistrationUpdate):
    try:
        id = await update_registration(id, enr)
        return id
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_registration_bjkk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# other


@router.post("/confirm/{id}", status_code=201)
async def api_confirm_registration(id: str, bt: BackgroundTasks):
    try:
        await confirm_registration(id, bt)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call confirm_registration")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/idbel/{id}", response_model=IdReply)
async def api_lookup_idbel(id: str):
    try:
        return await lookup_idbel(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call lookup_idbel")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/idfide/{id}", response_model=IdReply)
async def api_lookup_idfide(id: str):
    try:
        return await lookup_idfide(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call lookup_idfide")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/photo/{id}")
async def api_anon_upload_photo(id: str, body: dict):
    try:
        return await upload_photo(id, body["photo"])
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call upload_photo")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/photo/{id}")
async def api_anon_get_photo(id: str):
    try:
        return await get_photo(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_photo")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/notconfirmed_vk")
async def api_get_notconfirmed_vk():
    try:
        return await send_notconfirmed_vk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_photo")
        raise HTTPException(status_code=500, detail="Internal Server Error")
