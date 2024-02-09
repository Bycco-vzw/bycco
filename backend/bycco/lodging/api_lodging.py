# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
import base64
import asyncio
from typing import List
from fastapi import HTTPException, BackgroundTasks, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema
from reddevil.core import validate_token

router = APIRouter(prefix="/api/v1/lodging")

from bycco.lodging.lodging import (
    assign_room,
    make_reservation,
    get_lodging,
    get_lodgings,
    unassign_room,
    update_lodging,
    xls_lodgings,
)
from bycco.lodging.md_lodging import (
    Lodging,
    LodgingIn,
)

logger = logging.getLogger("bycco")


@router.post("/cmd/make_reservation", response_model=str)
async def api_make_reservation(ri: LodgingIn, bt: BackgroundTasks):
    try:
        return await make_reservation(ri, bt)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_reservation")
        raise HTTPException(status_code=500)


@router.get("/reservation", response_model=List[Lodging])
async def api_mgmt_get_reservations(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await get_lodgings()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call mgmt_get_reservation")
        raise HTTPException(status_code=500)


@router.get("/reservation/{id}", response_model=Lodging)
async def api_get_reservation(id: str):
    try:
        return await get_lodging(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_reservation")
        raise HTTPException(status_code=500)


@router.put("/reservation/{id}", response_model=Lodging)
async def api_update_reservation(id: str, reservation: Lodging):
    try:
        logger.info(f"api update rsv {reservation}")
        return await update_lodging(id, reservation)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_reservation")
        raise HTTPException(status_code=500)


@router.post("/cmd/assignroom/{id}/{roomnr}", response_model=Lodging)
async def api_assign_room(id: str, roomnr: str):
    try:
        logger.info(f"assign room {roomnr}")
        return await assign_room(id, roomnr)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call assign_room")
        raise HTTPException(status_code=500)


@router.delete("/cmd/unassignroom/{id}/{roomnr}", response_model=Lodging)
async def api_unassign_room(id: str, roomnr: str):
    try:
        logger.info(f"unassign roomnumber {roomnr}")
        return await unassign_room(id, roomnr)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call unassign")
        raise HTTPException(status_code=500)


# @app.get("/api/v1/xls/reservation")
# async def api_xls_reservations(
#     auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
# ):
#     await validate_token(auth)
#     try:
#         xlsfile = await xls_reservations()
#         return {"xls64": base64.b64encode(xlsfile)}
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         logger.exception("failed api call xls")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
