from typing import List
from .md_statamic import BucketFolder


def get_bucketoverview() -> List(BucketFolder):
    bl = [BucketFolder(
        group='pages',
        names = get_foldername('pages'),
        filetype = "md"
        nature = "content"
        archivename="archive/pages/{name}"       
    )]
