# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema, validate_token

from . import upload_jsonfile, TrnUpload, TrnUnofficialResult, set_unofficial_result

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/tournament")


# test endpoints


@router.post("/json", status_code=201)
async def api_upload_jsonfile(
    trn: TrnUpload,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await upload_jsonfile(trn)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call upload_jsonfile")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/unofficial_result", status_code=201)
async def api_set_unofficial_result(
    ur: TrnUnofficialResult,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        set_unofficial_result(ur)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call set_unofficial_result")
        raise HTTPException(status_code=500, detail="Internal Server Error")
