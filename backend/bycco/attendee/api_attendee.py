# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from typing import List
from fastapi import HTTPException, BackgroundTasks, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from reddevil.core import RdException, bearer_schema
from reddevil.core import validate_token

router = APIRouter(prefix="/api/v1/attendee")

from . import (
    Attendee,
    AttendeeItem,
    add_attendees_vk,
    get_attendee_vk,
    get_attendees_vk,
    update_update_bjk,
)

logger = logging.getLogger(__name__)

# vk


@router.get("/vk", response_model=List[AttendeeItem])
async def api_get_attendees_vk():
    try:
        return await get_attendees_vk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_attendees_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/vk/{id}", response_model=Attendee)
async def api_get_attendees_vk(id: str):
    try:
        return await get_attendee_vk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_attendees_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/vk", response_model=str)
async def api_add_attendee_vk(enr: Attendee):
    try:
        id = await add_attendees_vk(enr)
        return id
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call add_attendee_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/vk/{id}", response_model=Attendee)
async def api_update_attendee_vk(id: str, enr: Attendee):
    try:
        id = await api_update_attendee_vk(id, enr)
        return id
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_attendee_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/badges_vk", response_class=HTMLResponse)
async def api_generate_badges():
    try:
        return await generate_badges_vk(cat)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call generate_namecards")
        raise HTTPException(status_code=500, detail="Internal Server Error")
