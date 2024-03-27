# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2024

import logging

# from reddevil.filestore.filestore import list_bucket_files
from bycco.statamic import empty_dir

logger = logging.getLogger(__name__)


async def copy_pages_to_statamic(st_instance: str):
    """
    copy pages to
    """
    path = f"{st_instance}/content/collections/pages"
    await empty_dir(path)
    # files = list_bucket_files("pages")
