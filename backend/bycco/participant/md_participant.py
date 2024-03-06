# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from typing import Dict, Any, List, Optional, Type, Union
from enum import Enum
from pydantic import BaseModel, Field
from reddevil.core import DbBase


class ParticipantVKCategory(str, Enum):
    VK2024 = "VK"
    SEN2024 = "SEN"
    EXP2024 = "EXP"


class ParticipantBJKCategory(str, Enum):
    U8 = "U8"
    U10 = "U10"
    U12 = "U12"
    U14 = "U14"
    U16 = "U16"
    U18 = "U18"
    U20 = "U20"


class Gender(str, Enum):
    M = "M"
    F = "F"


class NatStatus(str, Enum):
    fidebelg = "Fide Belg."
    nobelg = "No Belg."
    unknown = "Unknown"


class ParticipantVKDB(BaseModel):
    """
    the enrollment model as used in the database
    is normally not exposed
    """

    badgemimetype: str
    badgeimage: bytes
    badgelength: int
    birthyear: int
    category: ParticipantVKCategory
    chesstitle: str
    custom: str | None
    enabled: bool
    email: List[str]
    first_name: str
    gender: Gender
    idbel: str
    idclub: str | None
    idfide: str | None
    locale: str
    last_name: str
    natstatus: str
    present: datetime | None
    ratingbel: int
    ratingfide: int
    remarks: str
    _id: str
    _version: int
    _documenttype: str
    _creationtime: datetime
    _modificationtime: datetime


class ParticipantVKItem(BaseModel):
    """
    validator for public view of a enrollment
    """

    badgelength: int | None = 0
    birthyear: int
    category: ParticipantVKCategory
    chesstitle: str | None
    first_name: str
    gender: Gender
    id: str
    idbel: str
    idclub: str | None
    idfide: str | None
    last_name: str
    nationalityfide: str
    ratingbel: int = 0
    ratingfide: int = 0


class DbParticpantVK(DbBase):
    COLLECTION = "participant_vk"
    DOCUMENTTYPE = ParticipantVKDB
    VERSION = 1
