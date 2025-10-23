# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2014

import logging
import json
from binascii import a2b_base64
from io import BytesIO, StringIO
from reddevil.filestore.filestore import (
    write_bucket_content,
    read_bucket_content,
)
from . import TrnUpload, TrnUnofficialResult

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


def set_unofficial_result(ur: TrnUnofficialResult) -> None:
    """
    set  the unofficial result in json file
    """
    logger.info(f"setting unofficial result {ur}")
    try:
        jf = read_bucket_content(f"trn/{ur.name}")
    except Exception:
        logger.info(f"failed to read {ur.name}")
    trn = json.loads(jf)
    players = trn["Swar"]["Player"]
    for p in players:
        rounds = p["RoundArray"]
        for r in rounds:
            if r["RoundNr"] != ur.round:
                continue
            if r["Tabel"] != str(ur.boardnr):
                continue
            if r["Color"] == "White":
                logger.info(f"setting unofficial result for {ur.name} round {ur.round}")
                r["UnofficialResult"] = ur.unofficial_result
    njf = StringIO(json.dumps(trn))
    try:
        write_bucket_content(f"trn/{ur.name}", njf)
    except Exception as e:
        logger.info(f"failed to write {ur.name}")
        logger.exception(e)
