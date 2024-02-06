# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema, validate_token
from typing import List
from bycco.room.md_room import Room, RoomDB, RoomItem, DbRoom
from bycco.room.room import get_rooms, get_room, get_free_rooms, roominit

router = APIRouter(prefix="/api/v1/room")

logger = logging.getLogger("bycco")


@router.get("/room", response_model=List[RoomItem])
async def api_get_rooms(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await get_rooms()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_rooms")
        raise HTTPException(status_code=500)


@router.get("/room/{id}", response_model=Room)
async def api_get_room(
    id: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await get_room(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_room")
        raise HTTPException(status_code=500)


@router.post("/roominit", status_code=201, include_in_schema=False)
async def api_roominit(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        return await roominit("room2024.csv")
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_room")
        raise HTTPException(status_code=500)


@router.get("/freeroom/{roomtype}", response_model=List[RoomItem])
async def api_get_free_rooms(roomtype: str):
    try:
        return await get_free_rooms(roomtype)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_free_rooms")
        raise HTTPException(status_code=500)
