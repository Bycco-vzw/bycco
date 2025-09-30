# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2024

from datetime import datetime
from typing import Dict, Any, List, Optional, Type, Union
from enum import Enum
from pydantic import BaseModel
from reddevil.core import DbBase


class AttendeeCategory(str, Enum):
    U8 = "B8"
    U10 = "B10"
    U12 = "B12"
    U14 = "B14"
    U16 = "B16"
    U18 = "B18"
    U20 = "B20"
    ARB = "ARB"
    EXP = "EXP"
    VK = "VK"
    SEN = "SEN"
    ORG = "ORG"
    EAT = "EAT"
    GST = "GST"


class Gender(str, Enum):
    M = "M"
    F = "F"


class Attendee(BaseModel):
    """
    The model used to make badge
    """

    category: AttendeeCategory | None = None
    first_name: str | None = None
    id: str | None = None
    last_name: str | None = None


class AttendeeItem(BaseModel):
    """
    an list item of an Attendee
    """

    category: AttendeeCategory | None
    first_name: str | None
    id: str | None
    last_name: str | None


class AttendeeUpdate(BaseModel):
    """
    validator for attendee updates
    """

    badgemimetype: str | None
    badgeimage: bytes | None
    badgelength: int | None
    birthyear: int | None
    category: AttendeeCategory | None
    chesstitle: str | None
    custom: str | None
    first_name: str | None
    gender: Gender | None
    id: str | None
    idbel: str | None
    idclub: str | None
    idfide: str | None
    locale: str | None
    last_name: str | None
    meals: str | None
    rating: int | None
    remarks: str | None


class DbAttendee(DbBase):
    COLLECTION = "attendee"
    DOCUMENTTYPE = Attendee
    VERSION = 1
