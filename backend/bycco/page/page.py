# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2024

import logging
from asyncio import sleep
from asyncssh import constants
from io import BytesIO

# from reddevil.filestore.filestore import list_bucket_files
from bycco.statamic import (
    empty_dir,
    get_file,
    put_file,
    list_files,
    ReadRequest,
)
from reddevil.filestore.filestore import (
    list_bucket_files,
    read_bucket_content,
    write_bucket_content,
)


logger = logging.getLogger(__name__)


async def checkin(st_instance: str) -> None:
    """
    copy pages from the GCP bucket to
    the pages collection of statamic
    """
    # empty statamic pages collection
    path = f"{st_instance}/content/collections/pages"
    await empty_dir(path)
    # get all bucket pages
    files = list_bucket_files("pages")
    for f in files:
        # read the content per file
        content = read_bucket_content(f)
        # write it in the statamic collection
        fname = f.split("/")[1]
        path = f"{st_instance}/content/collections/pages/{fname}"
        await put_file(path, content, "wb")


async def checkout(st_instance: str) -> None:
    """
    copy pages from statamic pages collection
    to the GCP bucket
    """
    # empty statamic pages collection
    path = f"{st_instance}/content/collections/pages"
    # get all statamic pages
    files = await list_files(path)
    for f in files:
        if f.attrs.type != constants.FILEXFER_TYPE_REGULAR:
            logger.info(f"skipping {f.filename}")
            continue
        logger.info(f"copying {f.filename}")
        rrq = ReadRequest(name=f"{path}/{f.filename}", binary=True)
        fc = BytesIO(await get_file(rrq))
        try:
            write_bucket_content(f"pages/{f.filename}", fc)
        except Exception as e:
            logger.info(f"failed to write {f.filename}")
            logger.exception(e)
