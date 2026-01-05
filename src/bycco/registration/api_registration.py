# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
import base64

from fastapi import HTTPException, BackgroundTasks, APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema, validate_token


from bycco.registration import (
    RegistrationIn,
    RegistrationItem,
    RegistrationNoBadge,
    RegistrationUpdate,
    IdReply,
    confirm_registration,
    create_registration,
    get_registration,
    get_registrations,
    get_photo,
    lookup_idbel,
    lookup_idfide,
    update_registration,
    upload_photo,
    xls_registration,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/registration")

# bjk


@router.get("/bjk", response_model=list[RegistrationItem])
async def api_get_registrations():
    try:
        return await get_registrations()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_registrations_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/bjk/{id}", response_model=RegistrationNoBadge)
async def api_get_registration(id: str):
    try:
        reg = await get_registration(id)
        return reg
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_registration")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/bjk", response_model=str)
async def api_create_registration(reg: RegistrationIn):
    try:
        id = await create_registration(reg)
        return id
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call create_registration_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/bjk/{id}")
async def api_update_registration_vk(id: str, reg: RegistrationUpdate):
    try:
        await update_registration(id, reg)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call create_registrationk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# other


@router.post("/confirm/{id}", status_code=201)
async def api_confirm_registration(id: str, bt: BackgroundTasks):
    try:
        await confirm_registration(id, bt)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call confirm_registration")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/idbel/{id}", response_model=IdReply)
async def api_lookup_idbel(id: str):
    try:
        return await lookup_idbel(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call lookup_idbel")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/idfide/{id}", response_model=IdReply)
async def api_lookup_idfide(id: str):
    try:
        return await lookup_idfide(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call lookup_idfide")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/photo/{id}")
async def api_anon_upload_photo(id: str, body: dict):
    try:
        return await upload_photo(id, body["photo"])
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call upload_photo")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/photo/{id}")
async def api_anon_get_photo(id: str):
    try:
        return await get_photo(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_photo")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/cmd/xls_registration")
async def api_xls_registration(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    await validate_token(auth)
    try:
        xlsfile = await xls_registration()
        return {"xls64": base64.b64encode(xlsfile)}
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call xls")
        raise HTTPException(status_code=500, detail="Internal Server Error")
