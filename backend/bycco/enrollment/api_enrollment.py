# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
import base64
import asyncio
from typing import Optional
from fastapi import HTTPException, BackgroundTasks, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema
from reddevil.core import validate_token

router = APIRouter(prefix="/api/v1/enrollment")

from bycco.enrollment import (
    EnrollmentVkIn,
    EnrollmentIn,
    IdReply,
    confirm_enrollment,
    create_enrollment_vk,
    create_enrollment_bjk,
    get_photo,
    lookup_idbel,
    lookup_idfide,
    upload_photo,
)

logger = logging.getLogger(__name__)

# vk


@router.post("/vk", response_model=str)
async def api_create_enrollment_vk(enr: EnrollmentVkIn):
    try:
        id = await create_enrollment_vk(enr)
        return id
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_enrollment_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# bjk


@router.post("/bjk", response_model=str)
async def api_create_enrollment_bjk(enr: EnrollmentIn):
    try:
        id = await create_enrollment_bjk(enr)
        return id
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_enrollment_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# other


@router.post("/confirm/{id}", status_code=201)
async def api_confirm_enrollment(id: str, bt: BackgroundTasks):
    try:
        await confirm_enrollment(id, bt)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call confirm_enrollment")
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


# @router.get("", response_model=EnrollmentList)
# async def api_get_enrollments(
#     auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
# ):
#     try:
#         await validate_token(auth)
#         return await get_enrollments({"_class": EnrollmentOut})
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         log.exception("failed api call get_enrollments")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


# @router.get("/api/v1/enrollment/{id}", response_model=Enrollment)
# async def api_get_enrollment(
#     id: str, auth: HTTPAuthorizationCredentials = Depends(bearer_schema)
# ):
#     log.info(f"get enrollment {id} {auth}")
#     try:
#         await validate_token(auth)
#         a = await get_enrollment(id, {"_class": EnrollmentOut})
#         log.info(f"a: {a}")
#         return a
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         log.exception("failed api call get_enrollment")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


# @router.delete("/api/v1/enrollment/{id}")
# async def api_delete_enrollment(
#     id: str, auth: HTTPAuthorizationCredentials = Depends(bearer_schema)
# ):
#     await validate_token(auth)
#     try:
#         await disable_enrollment(id)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         log.exception("failed api call delete_enrollment")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


# @router.put("/api/v1/enrollment/{id}")
# async def api_update_enrollment(
#     id: str,
#     s: EnrollmentUpdate,
#     auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
# ):
#     try:
#         await validate_token(auth)
#         await update_enrollment(id, s)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         log.exception("failed api call update_enrollment")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


# @router.get("/api/v1/xls/enrollment")
# async def api_xls_enrollments(
#     auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
# ):
#     await validate_token(auth)
#     try:
#         xlsfile = await xls_enrollments()
#         return {"xls64": base64.b64encode(xlsfile) }
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         log.exception("failed api call get_enrollments")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
