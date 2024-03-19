# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from typing import List
from reddevil.core import RdException, get_settings, bearer_schema, validate_token

from bycco.main import app
from . import (
    create_pr_lodging,
    create_pr_participant_bjk,
    create_pr_participant_vk,
    create_pr_participants_bjk,
    create_pr_participants_vk,
    delete_pr_lodging,
    delete_pr_participant_bjk,
    delete_pr_participant_vk,
    email_paymentrequest,
    email_paymentrequests,
    get_payment_requests,
    get_payment_request,
    update_payment_request,
    update_pr_lodging,
    update_pr_participant_bjk,
    update_pr_participant_vk,
    PaymentRequest,
    PaymentRequestItem,
)


logger = logging.getLogger("bycco")
router = APIRouter(prefix="/api/v1/payment")
settings = get_settings()

# general


@router.get("/pr/{prqid}", response_model=PaymentRequest)
async def api_mgmt_get_paymentrequests(
    prqid: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await get_payment_request(prqid)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_payment_request")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/pr", response_model=List[PaymentRequestItem])
async def api_mgmt_get_paymentrequests(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await get_payment_requests()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_payment_request")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/pr/{id}", response_model=PaymentRequest)
async def api_update_paymentrequest(
    id: str,
    prq: PaymentRequest,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await update_payment_request(id, prq)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call update payment_request")
        raise HTTPException(status_code=500)


@router.post("/email_pr/{id}")
async def api_email_paymentrequest(
    id: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await email_paymentrequest(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_pr_reservation")
        raise HTTPException(status_code=500)


@router.post("/email_pr")
async def api_email_paymentrequest(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await email_paymentrequests(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_pr_reservation")
        raise HTTPException(status_code=500)


# lodging


@router.post("/lodging_pr/{id}", response_model=str)
async def api_create_pr_lodging(
    id: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await create_pr_lodging(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_pr_reservation")
        raise HTTPException(status_code=500)


@router.put("/lodging_pr/{id}")
async def api_update_pr_lodging(
    id: str,
    prq: PaymentRequest,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await update_pr_lodging(id, prq)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call update_pr_reservation")
        raise HTTPException(status_code=500)


@router.delete("/lodging_pr/{id}")
async def api_delete_pr_lodging(
    id: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await delete_pr_lodging(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call delete_pr_reservation")
        raise HTTPException(status_code=500)


# vk


@router.post("/participant_vk_pr/{id}", response_model=str)
async def api_create_pr_participant_vk(
    id: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await create_pr_participant_vk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_pr_reservation")
        raise HTTPException(status_code=500)


@router.post("/participant_vk_pr", status_code=201)
async def api_create_pr_participant_vk(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await create_pr_participants_vk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_pr_reservation")
        raise HTTPException(status_code=500)


@router.put("/participant_vk_pr/{id}")
async def api_update_pr_participant_vk(
    id: str,
    prq: PaymentRequest,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await update_pr_participant_vk(id, prq)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call update_pr_reservation")
        raise HTTPException(status_code=500)


@router.delete("/participant_vk_pr/{id}")
async def api_delete_pr_participant_vk(
    id: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await delete_pr_participant_vk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call delete_pr_reservation")
        raise HTTPException(status_code=500)


# bjk


@router.post("/participant_bjk_pr/{id}", response_model=str)
async def api_create_pr_participant_bjk(
    id: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await create_pr_participant_bjk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_pr_reservation")
        raise HTTPException(status_code=500)


@router.post("/participant_bjk_pr", status_code=201)
async def api_create_pr_participant_bjk(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await create_pr_participants_bjk()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call create_pr_reservation")
        raise HTTPException(status_code=500)


@router.put("/participant_bjk_pr/{id}")
async def api_update_pr_participant_bjk(
    id: str,
    prq: PaymentRequest,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await update_pr_participant_bjk(id, prq)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call update_pr_reservation")
        raise HTTPException(status_code=500)


@router.delete("/participant_bjk_pr/{id}")
async def api_delete_pr_participant_bjk(
    id: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await delete_pr_participant_bjk(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call delete_pr_reservation")
        raise HTTPException(status_code=500)
