# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from typing import List
from reddevil.core import RdException, get_settings, bearer_schema, validate_token

from bycco.main import app
from . import (
    create_pr_enrollment,
    create_pr_lodging,
    delete_pr_enrollment,
    delete_pr_lodging,
    email_paymentrequest,
    get_payment_requests,
    get_payment_request,
    update_payment_request,
    update_pr_enrollment,
    update_pr_lodging,
    PaymentRequest,
    PaymentRequestItem,
)


logger = logging.getLogger("bycco")
router = APIRouter(prefix="/api/v1/payment")
settings = get_settings()


@router.get("/pr/{prqid}", response_model=PaymentRequest)
async def api_get_paymentrequests(
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
async def api_get_paymentrequests(
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


@app.put("/pr/{id}", response_model=PaymentRequest)
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


# business methods pr reservation


@app.post("/lodging_pr/{id}", response_model=str)
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


@app.put("/lodging_pr/{id}", response_model=str)
async def api_update_pr_lodging(
    id: str,
    prq: PaymentRequest,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await update_pr_lodging(rsvid, prq)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call update_pr_reservation")
        raise HTTPException(status_code=500)


@app.delete("/lodging_pr/{id}")
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


@app.post("/email_pr/{id}")
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


# business methods pr enrollments


# @app.post("/api/v1/enr/paymentrequest/{enrid}", response_model=str)
# async def api_create_pr_enrollment(
#     enrid: str,
#     admincost: str = "#NA",
#     auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
# ):
#     try:
#         await validate_token(auth)
#         return await create_pr_enrollment(enrid, admincost=admincost)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         logger.exception("failed api call create_pr_enrollment")
#         raise HTTPException(status_code=500)


# @app.delete("/api/v1/enr/paymentrequest/{enrid}")
# async def api_delete_pr_enrollment(
#     enrid: str,
#     auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
# ):
#     try:
#         await validate_token(auth)
#         await delete_pr_enrollment(enrid)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         logger.exception("failed api call delete_pr_enrollment")
#         raise HTTPException(status_code=500)
