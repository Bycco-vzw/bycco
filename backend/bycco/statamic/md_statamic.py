# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2023

# all models in the service level exposed to the API
# we are using pydantic as tool

import logging

from reddevil.core import DbBase
from typing import Dict, Any, List, Optional, Type
from fastapi import File
from pydantic import BaseModel, Field


class BucketFolder(BaseModel):
    """
    contains a list of all the "folders" with their meaning
    """

    group: str
    names: List[str]
    filetype: str  # "md", 'yaml", ...
    nature: str  # "content", "asset"
    archivename: str
