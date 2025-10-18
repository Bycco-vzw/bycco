# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from typing import Dict, Any, List, Optional, Type, Union
from enum import Enum
from pydantic import BaseModel, Field
from reddevil.core import DbBase


class Guest(BaseModel):
    age_category: str | None = None
    birthdate: str | None
    first_name: str | None
    player: bool | None
    last_name: str | None
    meals: List[str] | None = None
    meals_wishes: str | None = None
    stay: str | None = None


class Assignment(BaseModel):
    roomnr: str | None
    roomtype: str | None
    guestlist: List[Guest] | None
    assignmentdate: datetime


class StayDB(BaseModel):
    """
    the stay model as used in the database
    is normally not exposed
    """

    address: str
    assignments: List[Assignment] | None = None
    bycco_remarks: str
    checkindate: str  # format YYYY-MM-DD
    checkoutdate: str  # format YYYY-MM-DD
    email: str  # comma separated list of email addresses
    enabled: bool
    first_name: str
    guestlist: List[Guest]
    locale: str
    stay: str
    logging: List[str]
    last_name: str
    meals: str  # comma separated list of MMDD-BLD
    mobile: str  # comma separeted list of free format mobile numbers
    number: int  # a sequence number
    organizers: bool
    payment_id: str
    remarks: str
    _id: str
    _version: int
    _documenttype: str
    _creationtime: datetime
    _modificationtime: datetime


class Stay(BaseModel):
    """
    Stay model, all fields optional
    """

    address: str | None = None
    assignments: List[Assignment] | None = None
    bycco_remarks: str | None = None
    checkindate: str | None = None
    checkoutdate: str | None = None
    email: str | None = None
    enabled: bool | None = None
    first_name: str | None = None
    guestlist: List[Guest] | None = None
    id: str | None = None
    last_name: str | None = None
    locale: str | None = None
    stay: str | None = None
    logging: List[str] | None = None
    meals: str | None = None
    mobile: str | None = None
    number: int | None = None
    organizers: bool | None = None
    payment_id: str | None = None
    remarks: str | None = None
    _id: str | None = None
    _version: int | None = None
    _documenttype: str | None = None
    _creationtime: datetime | None = None
    _modificationtime: datetime | None = None


class StayIn(BaseModel):
    address: str | None = ""
    checkindate: str | None
    checkoutdate: str | None
    email: str
    first_name: str
    guestlist: List[Guest]
    last_name: str
    locale: str | None
    stay: str | None
    meals: str | None
    mobile: str
    organizers: bool | None = None
    remarks: str | None


class StayList(BaseModel):
    stays: List[Any]


class DbStay(DbBase):
    COLLECTION = "stay2026"
    VERSION = 1
    IDGENERATOR = "uuid"
