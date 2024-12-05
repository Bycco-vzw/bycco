# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from reddevil.core import DbBase


class RegistrationCategory(str, Enum):
    U8 = "U8"
    U10 = "U10"
    U12 = "U12"
    U14 = "U14"
    U16 = "U16"
    U18 = "U18"
    U20 = "U20"
    ARB = "ARB"
    ORG = "ORG"
    OTHER = "OTH"
    # VK2024 = "VK"
    # SEN2024 = "SEN"
    # EXP2024 = "EXP"


class Gender(str, Enum):
    M = "M"
    F = "F"


class NatStatus(str, Enum):
    fidebelg = "Fide Belg."
    nobelg = "No Belg."
    unknown = "Unknown"


class RegistrationRepresentative(BaseModel):
    emailattendant: str | None
    emailparent: str | None
    fullnameattendant: str
    fullnameparent: str
    mobileattendant: str
    mobileparent: str


class RegistrationDB(BaseModel):
    """
    the registration model as used in the database
    is normally not exposed
    """

    badgemimetype: str
    badgeimage: bytes
    badgelength: int
    birthyear: int
    category: RegistrationCategory
    chesstitle: str
    confirmed: bool
    confirmation_email: datetime | None = None
    custom: str | None
    emailplayer: str | None
    enabled: bool
    event: str
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
    registrationtime: datetime | None = None
    representative: RegistrationRepresentative | None
    remarks: str
    _id: str
    _version: int
    _documenttype: str
    _creationtime: datetime
    _modificationtime: datetime


class RegistrationIn(BaseModel):
    """
    the model to create a registration
    """

    category: str
    emailparent: str
    emailplayer: str
    emailattendant: str
    fullnameattendant: str
    fullnameparent: str
    idbel: str
    idfide: str | None = None
    idsub: str | None = None
    locale: str
    mobileattendant: str
    mobileparent: str
    mobileplayer: str


class RegistrationVkIn(BaseModel):
    """
    the model to create a registration
    """

    category: str
    emailplayer: str
    idbel: str | None = None
    idfide: str | None = None
    idsub: str | None = None
    locale: str
    mobileplayer: str


class RegistrationItem(BaseModel):
    """
    validator for public view of a registration
    """

    badgelength: int | None = 0
    birthyear: int | None = 0
    category: RegistrationCategory | None = None
    confirmed: bool | None = False
    chesstitle: str | None = None
    confirmation_email: datetime | None = None
    enabled: bool = True
    first_name: str | None = None
    gender: Gender | None = None
    id: str
    idbel: str | None = None
    idclub: str | None = None
    idfide: str | None = None
    last_name: str | None = None
    nationalityfide: str | None = None
    ratingbel: int | None = 0
    ratingfide: int | None = 0
    registrationtime: datetime | None = None


class RegistrationUpdate(BaseModel):
    """
    the generic model for updates
    """

    badgemimetype: str | None = None
    badgeimage: bytes | None = None
    badgelength: int | None = None
    birthday: str | None = None
    birthyear: int | None = None
    category: RegistrationCategory | None = None
    chesstitle: str | None = None
    confirmed: bool | None = None
    custom: str | None = None
    emailplayer: str | None = None
    enabled: bool | None = None
    event: str | None = None
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
    rating: int | None = None
    ratingbel: int | None = None
    ratingfide: int | None = None
    registrationtime: datetime | None = None
    representative: RegistrationRepresentative | None = None
    remarks: str | None = None


class RegistrationNoBadge(BaseModel):
    """
    the internal model used everywhere
    """

    badgemimetype: str | None = None
    badgelength: int | None = None
    birthday: str | None = None
    birthyear: int | None = None
    category: RegistrationCategory | None = None
    chesstitle: str | None = None
    confirmation_email: datetime | None = None
    confirmed: bool | None = None
    custom: str | None = None
    emailplayer: str | None = None
    enabled: bool | None = True
    event: str | None = None
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
    rating: int | None = None
    ratingbel: int | None = None
    ratingfide: int | None = None
    registrationtime: datetime | None = None
    representative: RegistrationRepresentative | None = None
    remarks: str | None = None


class Registration(BaseModel):
    """
    the internal model used everywhere
    """

    badgemimetype: str | None = None
    badgeimage: bytes | None = None
    badgelength: int | None = None
    birthday: str | None = None
    birthyear: int | None = None
    category: RegistrationCategory | None = None
    chesstitle: str | None = None
    confirmation_email: datetime | None = None
    confirmed: bool | None = None
    custom: str | None = None
    emailplayer: str | None = None
    enabled: bool | None = True
    event: str | None = None
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
    rating: int | None = None
    ratingbel: int | None = None
    ratingfide: int | None = None
    registrationtime: datetime | None = None
    representative: RegistrationRepresentative | None = None
    remarks: str | None = None


class IdReply(BaseModel):
    age_ok: bool = True
    belfound: bool = False
    birthyear: int = 0
    chesstitle: str | None = None
    first_name: str | None = ""
    gender: Gender | None = None
    idbel: str | None = None
    idclub: str | None = None
    idfide: str | None = None
    last_name: str | None = ""
    nationalitybel: str = "BEL"
    nationalityfide: str = ""
    natstatus: NatStatus = NatStatus.unknown
    ratingbel: int | None = 0
    ratingfide: int | None = 0
    subconfirmed: bool = False
    subid: str | None = None


class DbRegistration(DbBase):
    COLLECTION = "registration"
    DOCUMENTTYPE = "Registration"
    VERSION = 1
