# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2024

import logging
from asyncio import sleep

# from reddevil.filestore.filestore import list_bucket_files
from bycco.statamic import (
    empty_dir,
    put_file,
    list_files,
)
from reddevil.filestore.filestore import list_bucket_files, read_bucket_content

logger = logging.getLogger(__name__)


async def copy_pages_to_statamic(st_instance: str) -> None:
    """
    copy pages from the GCP bucket
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


async def copy_pages_to_bucket(st_instance: str) -> None:
    """
    copy pages from statamic pages collection
    to the GCP bucket
    """
    # empty statamic pages collection
    path = f"{st_instance}/content/collections/pages"
    # get all statamic pages
    files = list_files(path)
    for f in files:
        logger.info(f"file {f}")
