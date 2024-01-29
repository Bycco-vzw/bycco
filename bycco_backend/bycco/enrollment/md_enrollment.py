# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from typing import Dict, Any, List, Optional, Type, Union
from enum import Enum
from pydantic import BaseModel, Field
from reddevil.core import DbBase


class EnrollmentCategory(str, Enum):
    B8 = "B8"
    B10 = "B10"
    B12 = "B12"
    B14 = "B14"
    B16 = "B16"
    B18 = "B18"
    B20 = "B20"
    G8 = "G8"
    G10 = "G10"
    G12 = "G12"
    G14 = "G14"
    G16 = "G16"
    G18 = "G18"
    G20 = "G20"
    ARB = "ARB"
    ORG = "ORG"
    OTHER = "OTH"
    VK2024 = "VK"
    SEN2024 = "SEN"
    EXP2024 = "EXP"


class Gender(str, Enum):
    M = "M"
    F = "F"


class NatStatus(str, Enum):
    fidebelg = "Fide Belg."
    nobelg = "No Belg."
    unknown = "Unknown"


class EnrollmentEvent(BaseModel):
    """
    event details
    """

    enddate: str | None
    eventtype: str | None
    startdate: str | None
    title: str | None
    options: dict | None


class EnrollmentRepresentative(BaseModel):
    emailattendant: str | None
    emailparent: str | None
    fullnameattendant: str
    fullnameparent: str
    mobileattendant: str
    mobileparent: str


class EnrollmentDB(BaseModel):
    """
    the enrollment model as used in the database
    is normally not exposed
    """

    badgemimetype: str
    badgeimage: bytes
    badgelength: int
    birthyear: int
    category: EnrollmentCategory
    chesstitle: str
    confirmed: bool
    custom: str | None
    emailplayer: str | None
    enabled: bool
    federation: str
    first_name: str
    gender: Gender
    idbel: str
    idclub: str | None
    idfide: str | None
    locale: str
    last_name: str
    mobileplayer: str
    nationalitybel: str
    nationalityfide: str
    natstatus: str
    present: datetime | None
    rating: int
    ratingbel: int
    ratingfide: int
    registrationtime: datetime
    representative: EnrollmentRepresentative | None
    remarks: str
    enrollmentevent: EnrollmentEvent
    _id: str
    _version: int
    _documenttype: str
    _creationtime: datetime
    _modificationtime: datetime


class EnrollmentIn(BaseModel):
    """
    the model to create a enrollment
    """

    category: str
    emailparent: str
    emailplayer: str
    emailattendant: str
    fullnameattendant: str
    fullnameparent: str
    idbel: str
    locale: str
    mobileattendant: str
    mobileparent: str
    mobileplayer: str


class EnrollmentVkIn(BaseModel):
    """
    the model to create a enrollment
    """

    category: str
    emailplayer: str
    idbel: str | None = None
    idfide: str | None = None
    idsub: str | None = None
    locale: str
    mobileplayer: str


class EnrollmentPublic(BaseModel):
    """
    validator for public view of a enrollment
    """

    badgelength: Optional[int] = 0
    birthyear: int
    category: EnrollmentCategory
    chesstitle: str | None
    first_name: str
    gender: Gender
    id: str
    idbel: str
    idclub: str | None
    idfide: str | None
    last_name: str
    nationalityfide: str
    rating: int = 0
    ratingbel: int = 0
    ratingfide: int = 0


class EnrollmentList(BaseModel):
    """
    a list view of enrollments
    """

    enrollments: List[EnrollmentPublic]


class EnrollmentVKOut(BaseModel):
    """
    validator for ouput
    """

    badgelength: int = 0
    birthyear: int
    category: EnrollmentCategory
    chesstitle: str | None
    confirmed: bool = False
    custom: str | None
    emailplayer: str | None
    enabled: Optional[bool]
    federation: str | None
    first_name: str
    gender: Gender
    id: str
    idbel: str
    idclub: str | None
    idfide: str | None
    locale: str
    last_name: str
    mobileplayer: str
    nationalitybel: str
    nationalityfide: str
    natstatus: str | None
    payment_id: str | None = ""
    present: datetime | None
    rating: int = 0
    ratingbel: int = 0
    ratingfide: int = 0
    registrationtime: datetime | None = None
    remarks: str = ""


class EnrollmentOut(BaseModel):
    """
    validator for ouput
    """

    badgelength: int = 0
    birthday: str | None
    birthyear: int
    category: EnrollmentCategory
    chesstitle: str | None
    confirmed: bool = False
    custom: str | None
    emailattendant: str | None
    emailparent: str | None
    emailplayer: str | None
    enabled: Optional[bool]
    federation: str | None
    first_name: str
    fullnameattendant: str
    fullnameparent: str
    gender: Gender
    id: str
    idbel: str
    idclub: str
    idfide: str | None
    locale: str
    last_name: str
    mobileattendant: str
    mobileparent: str
    mobileplayer: str
    nationalitybel: str
    nationalityfide: str
    natstatus: str | None
    payment_id: str | None = ""
    present: datetime | None
    rating: int = 0
    ratingbel: int = 0
    ratingfide: int = 0
    registrationtime: datetime | None = None
    remarks: str = ""


class EnrollmentUpdate(BaseModel):
    """
    the generic model for updates
    """

    badgemimetype: str | None = None
    badgeimage: Optional[bytes] = None
    badgelength: Optional[int] = None
    birthday: str | None = None
    birthyear: Optional[int] = None
    category: Optional[EnrollmentCategory] = None
    chesstitle: str | None = None
    confirmed: Optional[bool] = None
    custom: str | None = None
    emailplayer: str | None = None
    enabled: Optional[bool] = None
    federation: str | None = None
    first_name: str | None = None
    gender: str | None = None
    idbel: str | None = None
    idclub: str | None = None
    idfide: str | None = None
    last_name: str | None = None
    locale: str | None = None
    mobileplayer: str | None = None
    nationalitybel: str | None = None
    nationalityfide: str | None = None
    natstatus: str | None = NatStatus.unknown.value
    payment_id: str | None = None
    present: datetime | None = None
    rating: Optional[int] = None
    ratingbel: Optional[int] = None
    ratingfide: Optional[int] = None
    registrationtime: datetime | None = None
    representative: EnrollmentRepresentative | None = None
    remarks: str | None = None
    enrollmentevent: Optional[EnrollmentEvent] = None


class Enrollment(BaseModel):
    """
    the internal model used everywhere
    """

    badgemimetype: str | None = None
    badgeimage: Optional[bytes] = None
    badgelength: Optional[int] = None
    birthday: str | None = None
    birthyear: Optional[int] = None
    category: Optional[EnrollmentCategory] = None
    chesstitle: str | None = None
    confirmed: Optional[bool] = None
    custom: str | None = None
    emailplayer: str | None = None
    enabled: Optional[bool] = None
    federation: str | None = None
    first_name: str | None = None
    gender: str | None = None
    idbel: str | None = None
    idclub: str | None = None
    idfide: str | None = None
    id: str
    last_name: str | None = None
    locale: str | None = None
    mobileplayer: str | None = None
    nationalitybel: str | None = None
    nationalityfide: str | None = None
    natstatus: str | None = NatStatus.unknown.value
    payment_id: str | None = None
    present: datetime | None = None
    rating: Optional[int] = None
    ratingbel: Optional[int] = None
    ratingfide: Optional[int] = None
    registrationtime: datetime | None = None
    representative: EnrollmentRepresentative | None = None
    remarks: str | None = None
    enrollmentevent: Optional[EnrollmentEvent] = None


class IdReply(BaseModel):
    age_ok: bool = True
    belfound: bool = False
    birthyear: int = 0
    first_name: str | None = ""
    gender: Gender | None = None
    idbel: str | None = None
    idclub: str | None = None
    idfide: str | None = None
    last_name: str | None = ""
    nationalitybel: str = "BEL"
    nationalityfide: str = ""
    natstatus: NatStatus = NatStatus.unknown
    ratingbel: int = 0
    ratingfide: int = 0
    subconfirmed: bool = False
    subid: str | None = None


class DbEnrollment(DbBase):
    COLLECTION = "enrollment"
    DOCUMENTTYPE = "Enrollment"
    VERSION = 1
