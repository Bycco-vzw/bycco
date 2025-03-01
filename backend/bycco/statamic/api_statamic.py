# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from typing import Any

from reddevil.core import RdException, bearer_schema, validate_token

from . import get_file, put_file, ReadRequest, WriteRequest


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/statamic")


# test endpoints


@router.post("/get_file", response_model=Any)
async def api_get_file(
    rq: ReadRequest,
    # auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        # await validate_token(auth)
        return await get_file(rq)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_payment_request")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/put_file", status_code=201)
async def api_put_file(
    wr: WriteRequest,
    # auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        # await validate_token(auth)
        return await put_file(wr)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_payment_request")
        raise HTTPException(status_code=500, detail="Internal Server Error")
