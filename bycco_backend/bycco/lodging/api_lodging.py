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

router = APIRouter(prefix="/api/v1/lodging")

from bycco.lodging.lodging import (
    # assign_room,
    make_reservation,
    # get_reservation,
    # get_reservations,
    # unassign_room,
    # update_reservation,
    # xls_reservations,
)
from bycco.lodging.md_lodging import (
    Lodging,
    LodgingIn,
    LodgingList,
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


# @app.get("/api/v1/reservation", response_model=LodgingList)
# async def api_get_reservations(
#     auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
# ):
#     try:
#         await validate_token(auth)
#         return await get_reservations()
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         logger.exception("failed api call create_reservation")
#         raise HTTPException(status_code=500)


# @app.get("/api/v1/reservation/{id}", response_model=Reservation)
# async def api_get_reservation(id: str):
#     try:
#         return await get_reservation(id)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         logger.exception("failed api call create_reservation")
#         raise HTTPException(status_code=500)


# @app.put("/api/v1/reservation/{id}", response_model=Reservation)
# async def api_update_reservation(id: str, reservation: Reservation):
#     try:
#         logger.info(f"api rsv {reservation}")
#         return await update_reservation(id, reservation)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         logger.exception("failed api call create_reservation")
#         raise HTTPException(status_code=500)


# @app.put("/api/v1/rsv/assignroom/{id}/{roomnr}", response_model=Reservation)
# async def api_assign_room(id: str, roomnr: str, roomtype: Optional[str] = None):
#     try:
#         logger.info(f"assign roomtype {roomtype}")
#         return await assign_room(id, roomnr, roomtype=roomtype)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         logger.exception("failed api call assign_room")
#         raise HTTPException(status_code=500)


# @app.delete("/api/v1/rsv/assignroom/{id}/{roomnr}", response_model=Reservation)
# async def api_unassign_room(id: str, roomnr: str):
#     try:
#         logger.info(f"unassign roomnumber {roomnr}")
#         return await unassign_room(id, roomnr)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         logger.exception("failed api call unassign")
#         raise HTTPException(status_code=500)


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
