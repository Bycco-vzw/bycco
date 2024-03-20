# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
import asyncssh
from typing import Dict, Any
from datetime import date
from reddevil.core import get_secret

logger = logging.getLogger(__name__)

# crud


async def get_page(name: str) -> str:
    """
    get page from statamic
    """
    st_settings = get_secret("statamic")
    async with asyncssh.connect(
        st_settings["ssh-host"],
        username=st_settings["ssh-user"],
        password=st_settings["ssh-password"],
    ) as conn:
        async with conn.start_sftp_client() as sftp:
            async with sftp.open(name) as fd:
                content = await fd.read()
    return content
