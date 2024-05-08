# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from typing import List
from fastapi import HTTPException, BackgroundTasks, Depends, APIRouter
from fastapi.responses import HTMLResponse, Response
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema
from reddevil.core import validate_token

router = APIRouter(prefix="/api/v1/participant")

from . import (
    ParticipantBJKItem,
    ParticipantBJKDetail,
    ParticipantBJKUpdate,
    ParticipantVK,
    ParticipantVKItem,
    ParticipantVKDetail,
    generate_badges_bjk,
    generate_namecards_bjk,
    generate_namecards_vk,
    get_participants_bjk,
    get_participants_vk,
    get_participant_bjk,
    get_participant_vk,
    get_photo,
    import_participants_bjk,
    import_participants_vk,
    update_elo_bjk,
    update_elo_vk,
    update_participant_vk,
    update_participant_bjk,
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
        return await get_participant_vk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_particpant_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/vk/{id}", status_code=201)
async def api_mgmt_update_participants_vk(
    id: str,
    participant: ParticipantVK,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await update_participant_vk(id, participant)
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
        await import_participants_vk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call mgmt_import_enrollments_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/update/elo/vk", status_code=201)
async def api_mgmt_update_elo_vk(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        # await validate_token(auth)
        await update_elo_vk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call mgmt_update_elo_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/namecards_cat/vk/{cat}", response_class=HTMLResponse)
async def api_generate_namecards(cat: str):
    try:
        return await generate_namecards_vk(cat)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call generate_namecards")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/namecards_id/vk/{ids}", response_class=HTMLResponse)
async def api_generate_namecards(ids: str):
    try:
        return await generate_namecards_vk(cat="", ids=ids)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call generate_namecards")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# bjk


@router.get("/bjk", response_model=List[ParticipantBJKItem])
async def api_get_participants_bjk(enabled: str | None = None):
    try:
        if enabled:
            return await get_participants_bjk({"enabled": True})
        else:
            return await get_participants_bjk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_particpants_bjk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/bjk/{id}", response_model=ParticipantBJKDetail)
async def api_mgmt_get_participant_bjk(
    id: str, auth: HTTPAuthorizationCredentials = Depends(bearer_schema)
):
    try:
        # await validate_token(auth)
        return await get_participant_bjk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_particpant_bjk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/bjk/{id}", response_model=ParticipantBJKDetail)
async def api_mgmt_update_participant_bjk(
    id: str,
    participant: ParticipantBJKUpdate,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await update_participant_bjk(id, participant)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call update_participant_bjk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/import/enrollments/bjk", status_code=201)
async def api_mgmt_import_enrollments_bjk(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await import_participants_bjk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call mgmt_import_enrollments_bjk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/update/elo/bjk", status_code=201)
async def api_mgmt_update_elo_bjk(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        # await validate_token(auth)
        await update_elo_bjk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call mgmt_update_elo_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/namecards_cat/bjk/{cat}", response_class=HTMLResponse)
async def api_generate_namecards_cat(cat: str):
    try:
        return await generate_namecards_bjk(cat)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call generate_namecards")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/namecards_id/bjk/{ids}", response_class=HTMLResponse)
async def api_generate_namecards_ids(ids: str):
    try:
        return await generate_namecards_bjk(cat="", ids=ids)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call generate_namecards")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/badges_cat/bjk/{cat}", response_class=HTMLResponse)
async def api_generate_badges_cat(cat: str):
    try:
        return await generate_badges_bjk(cat)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call generate_namecards")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/badges_id/bjk/{ids}", response_class=HTMLResponse)
async def api_generate_badges_ids(ids: str):
    try:
        return await generate_badges_bjk(cat="", ids=ids)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call generate_namecards")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/photo/{id}", response_class=Response)
async def api_get_photo(id: str):
    try:
        return await get_photo(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_participant")
        raise HTTPException(status_code=500, detail="Internal Server Error")
