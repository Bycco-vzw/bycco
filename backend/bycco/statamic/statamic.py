# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2024

import logging
import asyncssh
from typing import Dict, Any
from datetime import date
from reddevil.core import get_secret

logger = logging.getLogger(__name__)

from . import ReadRequest


async def get_file(fr: ReadRequest) -> str:
    """
    get a file from statamic
    """
    st_settings = get_secret("statamic")
    async with asyncssh.connect(
        st_settings["ssh-host"],
        username=st_settings["ssh-user"],
        password=st_settings["ssh-password"],
    ) as conn:
        async with conn.start_sftp_client() as sftp:
            mode = "rb" if fr.binary else "r"
            async with sftp.open(fr.name, mode=mode) as fd:
                content = await fd.read()
    return content


async def put_file(name: str, content: Any) -> None:
    """
    put a page to statamic
    """
    st_settings = get_secret("statamic")
    async with asyncssh.connect(
        st_settings["ssh-host"],
        username=st_settings["ssh-user"],
        password=st_settings["ssh-password"],
    ) as conn:
        async with conn.start_sftp_client() as sftp:
            async with sftp.open(name, "w") as fd:
                await fd.write(content)


async def empty_dir(path: str) -> None:
    """
    empty a directory in statamic
    """
    mypath = f"{path}*" if path.endswith("/") else f"{path}/*"
    st_settings = get_secret("statamic")
    async with asyncssh.connect(
        st_settings["ssh-host"],
        username=st_settings["ssh-user"],
        password=st_settings["ssh-password"],
    ) as conn:
        result = await conn.run(f"rm {mypath}")
        logger.info(f"empty dir: {result} ")
