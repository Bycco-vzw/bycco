# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema, validate_token

from . import copy_pages_to_statamic, copy_pages_to_bucket


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/page")


# test endpoints


@router.post("/bucket_to_statamic/{st_instance}", status_code=201)
async def api_get_page(
    st_instance: str,
    # auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        # await validate_token(auth)
        await copy_pages_to_statamic(st_instance)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_payment_request")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/statamic_to_bucket/{st_instance}", status_code=201)
async def api_get_page(
    st_instance: str,
    # auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        # await validate_token(auth)
        await copy_pages_to_bucket(st_instance)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_payment_request")
        raise HTTPException(status_code=500, detail="Internal Server Error")
