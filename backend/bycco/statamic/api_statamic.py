import logging
from fastapi import HTTPException, Depends, APIRouter
from reddevil.core import RdException
from typing import List

from .md_statamic import BucketFolder
from .statamic import get_bucketoverview

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/statamic")


@router.get("/bucketoverview", response_model=List[BucketFolder])
async def api_get_bucketoverview():
    try:
        return await get_bucketoverview()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except
        logger.exception("failed api call anon_get_file")
        raise HTTPException(status_code=500, detail="Internal Server Error")

