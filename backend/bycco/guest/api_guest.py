# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from typing import List
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema
from reddevil.core import validate_token


from bycco.participant import (
    ParticipantBJKItem,
    ParticipantBJKDetail,
    ParticipantBJKUpdate,
    get_participants_bjk,
    get_participant_bjk,
    update_participant_bjk,
)
from . import add_guest

router = APIRouter(prefix="/api/v1/guest")
logger = logging.getLogger(__name__)


@router.get("", response_model=List[ParticipantBJKItem])
async def api_get_guests():
    try:
        return await get_participants_bjk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_guest")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{id}", response_model=ParticipantBJKDetail)
async def api_mgmt_get_guest(
    id: str, auth: HTTPAuthorizationCredentials = Depends(bearer_schema)
):
    try:
        await validate_token(auth)
        return await get_participant_bjk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_particpant_bjk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{id}", response_model=ParticipantBJKDetail)
async def api_mgmt_update_guest(
    id: str,
    participant: ParticipantBJKUpdate,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await update_participant_bjk(id, participant)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call update_participant_bjk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/{first_name}/{last_name}/{cat}", status_code=201)
async def api_mgmt_add_guest(
    first_name: str,
    last_name: str,
    cat: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await add_guest(first_name, last_name, cat)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call mgmt_add_guest")
        raise HTTPException(status_code=500, detail="Internal Server Error")
