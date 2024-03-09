# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from typing import List
from fastapi import HTTPException, BackgroundTasks, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema
from reddevil.core import validate_token

router = APIRouter(prefix="/api/v1/participant")

from . import (
    ParticipantBJKItem,
    ParticipantBJKDetail,
    ParticipantVKItem,
    ParticipantVKDetail,
    get_participants_bjk,
    get_participants_vk,
    mgmt_get_participant_bjk,
    mgmt_get_participant_vk,
    mgmt_import_enrollments_bjk,
    mgmt_import_enrollments_vk,
)

logger = logging.getLogger(__name__)

# vk


@router.get("/vk", response_model=List[ParticipantVKItem])
async def api_get_participants_vk():
    try:
        return await get_participants_vk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_particpants_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/vk/{id}", response_model=ParticipantVKDetail)
async def api_mgmt_get_participants_vk(
    id: str, auth: HTTPAuthorizationCredentials = Depends(bearer_schema)
):
    try:
        await validate_token(auth)
        return await mgmt_get_participant_vk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_particpant_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/import/enrollments/vk", status_code=201)
async def api_mgmt_import_enrollments_vk(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await mgmt_import_enrollments_vk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call mgmt_import_enrollments_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# bjk


@router.get("/bjk", response_model=List[ParticipantBJKItem])
async def api_get_participants_bjk():
    try:
        return await get_participants_bjk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_particpants_bjk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/bjk/{id}", response_model=ParticipantBJKDetail)
async def api_mgmt_get_participants_bjk(
    id: str, auth: HTTPAuthorizationCredentials = Depends(bearer_schema)
):
    try:
        await validate_token(auth)
        return await mgmt_get_participant_bjk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_particpant_bjk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/import/enrollments/bjk", status_code=201)
async def api_mgmt_import_enrollments_bjk(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await mgmt_import_enrollments_bjk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call mgmt_import_enrollments_bjk")
        raise HTTPException(status_code=500, detail="Internal Server Error")
