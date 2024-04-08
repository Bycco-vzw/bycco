# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2014

import logging
import io, csv
from typing import cast, List

from . import TrnUpload
from reddevil.core import RdBadRequest, get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def upload_jsonfile(tu: TrnUpload) -> None:
    """
    upload file to trn bucket
    """
    pass
