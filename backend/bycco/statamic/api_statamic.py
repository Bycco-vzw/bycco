# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema, validate_token

from . import (
    get_page,
)


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/statamic")


# test endpoints

@router.get("/page/{name}", response_model=str)
async def api_get_page(
    name: str,
    # auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        # await validate_token(auth)
        return await get_page(name)
    
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except:
        logger.exception("failed api call get_payment_request")
        raise HTTPException(status_code=500, detail="Internal Server Error")

