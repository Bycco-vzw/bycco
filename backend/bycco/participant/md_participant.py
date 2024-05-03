# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from typing import Dict, Any, List, Optional, Type, Union
from enum import Enum
from pydantic import BaseModel, Field
from reddevil.core import DbBase


class Gender(str, Enum):
    M = "M"
    F = "F"


class ParticipantVKCategory(str, Enum):
    VK2024 = "VK"
    SEN2024 = "SEN"
    EXP2024 = "EXP"


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
    enabled: bool
    emails: List[str]
    first_name: str
    gender: Gender
    idbel: str
    idclub: str | None
    idfide: str | None
    locale: str
    last_name: str
    nationalityfide: str | None
    payment_id: str | None = None
    present: datetime | None
    ratingbel: int
    ratingfide: int
    remarks: str
    _id: str
    _version: int
    _documenttype: str
    _creationtime: datetime
    _modificationtime: datetime


class ParticipantVKDetail(BaseModel):
    """
    the detailed participan model
    """

    badgemimetype: str
    badgelength: int
    birthyear: int
    category: ParticipantVKCategory
    chesstitle: str
    enabled: bool
    emails: List[str]
    first_name: str
    gender: Gender
    id: str
    idbel: str
    idclub: str | None
    idfide: str | None
    locale: str
    last_name: str
    nationalityfide: str | None
    payment_id: str | None = None
    present: datetime | None
    ratingbel: int
    ratingfide: int
    remarks: str


class ParticipantVK(BaseModel):
    """
    the participant model
    """

    badgemimetype: str | None = None
    badgelength: int | None = None
    birthyear: int | None = None
    category: ParticipantVKCategory | None = None
    chesstitle: str | None = None
    enabled: bool | None = None
    emails: List[str] | None = None
    first_name: str | None = None
    gender: Gender | None = None
    idbel: str | None = None
    idclub: str | None = None
    idfide: str | None = None
    locale: str | None = None
    last_name: str | None = None
    nationalityfide: str | None = None
    payment_id: str | None = None
    present: datetime | None = None
    ratingbel: int | None = None
    ratingfide: int | None = None
    remarks: str | None = None


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
    nationalityfide: str | None = "BEL"
    payment_id: str | None = None
    ratingbel: int | None = 0
    ratingfide: int | None = 0


class DbParticpantVK(DbBase):
    COLLECTION = "participant_vk"
    DOCUMENTTYPE = ParticipantVKDB
    VERSION = 1


### BJK


class NatStatus(str, Enum):
    fidebelg = "Fide Belg."
    nobelg = "No Belg."
    unknown = "Unknown"


class ParticipantBJKCategory(str, Enum):
    U8 = "U8"
    U10 = "U10"
    U12 = "U12"
    U14 = "U14"
    U16 = "U16"
    U18 = "U18"
    U20 = "U20"


class ParticipantBJKDB(BaseModel):
    """
    the participant model as used in the database
    is normally not exposed
    """

    badgemimetype: str
    badgeimage: bytes
    badgelength: int
    birthyear: int
    category: ParticipantBJKCategory
    chesstitle: str
    enabled: bool
    emails: List[str]
    first_name: str
    gender: Gender
    idbel: str
    idclub: str | None
    idfide: str | None
    locale: str
    last_name: str
    nationalityfide: str | None
    natstatus: NatStatus | None = NatStatus.unknown
    payment_id: str | None = None
    present: datetime | None
    ratingbel: int
    ratingfide: int
    remarks: str
    _id: str
    _version: int
    _documenttype: str
    _creationtime: datetime
    _modificationtime: datetime


class ParticipantBJKDetail(BaseModel):
    """
    the detailed participant model
    """

    badgemimetype: str
    badgelength: int
    birthyear: int
    category: ParticipantBJKCategory
    chesstitle: str
    enabled: bool
    emails: List[str]
    first_name: str
    gender: Gender
    id: str
    idbel: str
    idclub: str | None
    idfide: str | None
    locale: str
    last_name: str
    nationalityfide: str | None
    natstatus: NatStatus | None = NatStatus.unknown
    payment_id: str | None = None
    present: datetime | None
    ratingbel: int
    ratingfide: int
    remarks: str
    creationtime: datetime = Field(alias="_creationtime")


class ParticipantBJKUpdate(BaseModel):
    """
    participant update model
    """

    birthyear: int | None = None
    category: ParticipantBJKCategory | None = None
    chesstitle: str | None = None
    enabled: bool | None = None
    emails: List[str] | None = None
    first_name: str | None = None
    gender: Gender | None = None
    idbel: str | None = None
    idclub: str | None = None
    idfide: str | None = None
    locale: str | None = None
    last_name: str | None = None
    nationalityfide: str | None = None
    natstatus: NatStatus | None = None
    payment_id: str | None = None
    present: datetime | None = None
    ratingbel: int | None = None
    ratingfide: int | None = None
    remarks: str | None = None


class ParticipantBJK(BaseModel):
    """
    the participant model
    """

    badgemimetype: str | None = None
    badgelength: int | None = None
    birthyear: int | None = None
    category: ParticipantBJKCategory | None = None
    chesstitle: str | None = None
    enabled: bool | None = None
    emails: List[str] | None = None
    first_name: str | None = None
    gender: Gender | None = None
    idbel: str | None = None
    idclub: str | None = None
    idfide: str | None = None
    locale: str | None = None
    last_name: str | None = None
    nationalityfide: str | None = None
    payment_id: str | None = None
    present: datetime | None = None
    ratingbel: int | None = None
    ratingfide: int | None = None
    remarks: str | None = None


class ParticipantBJKItem(BaseModel):
    """
    validator for public view of a enrollment
    """

    badgelength: int | None = 0
    birthyear: int
    category: ParticipantBJKCategory
    chesstitle: str | None
    enabled: bool | None = True
    first_name: str
    gender: Gender
    id: str
    idbel: str
    idclub: str | None
    idfide: str | None
    last_name: str
    nationalityfide: str | None = "BEL"
    natstatus: NatStatus | None = NatStatus.unknown
    payment_id: str | None = None
    ratingbel: int | None = 0
    ratingfide: int | None = 0


class DbParticpantBJK(DbBase):
    COLLECTION = "participant_bjk"
    DOCUMENTTYPE = ParticipantBJKDB
    VERSION = 1


class PartTest(BaseModel):
    email: str = "@"
    ct: str = Field(alias="_ct", default="aha")
