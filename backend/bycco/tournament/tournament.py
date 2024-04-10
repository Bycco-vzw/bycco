# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2014

import logging
from binascii import a2b_base64
from io import BytesIO
from reddevil.filestore.filestore import (
    write_bucket_content,
)
from . import TrnUpload

logger = logging.getLogger(__name__)


async def upload_jsonfile(tu: TrnUpload) -> None:
    """
    upload file to trn bucket
    """
    header, data = tu.jsoncontent.split(",")
    fj = BytesIO(a2b_base64(data))
    logger.info(f"name: {tu.name}")
    try:
        write_bucket_content(f"trn/{tu.name}", fj)
    except Exception as e:
        logger.info(f"failed to write {tu.name}")
        logger.exception(e)
