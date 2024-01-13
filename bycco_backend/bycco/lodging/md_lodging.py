# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from typing import Dict, Any, List, Optional, Type, Union
from enum import Enum
from pydantic import BaseModel, Field
from reddevil.core import DbBase

class Guest(BaseModel):
    age_category: str | None
    birthday: str | None
    first_name:str | None
    player:bool | None
    last_name:str | None
    meals:List[str] | None
    meals_wishes:str | None
    lodging:str | None


class Assignment(BaseModel):
    roomnr:str | None
    roomtype:str | None
    guestlist:List[Guest] | None
    assignmentdate: datetime


class LodgingDB(BaseModel):
    """
    the reservation model as used in the database
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
    lodging: str
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


class Lodging(BaseModel):
    """
    Lodging model, all fields optional
    """

    address:str | None
    assignments:List[Assignment] | None
    bycco_remarks:str | None
    checkindate:str | None
    checkoutdate:str | None
    email:str | None
    enabled:bool | None
    first_name:str | None
    guestlist:List[Guest] | None
    id:str | None
    last_name:str | None
    locale:str | None
    lodging:str | None
    logging:List[str] | None
    meals:str | None
    mobile:str | None
    number:int | None
    organizers:bool | None
    payment_id:str | None
    remarks:str | None
    _version:int | None
    _documenttype:str | None
    creationtime:datetime | None = Field(alias="_creationtime")
    modificationtime:datetime | None = Field(alias="_modificationtime")


class LodgingIn(BaseModel):
    address:str | None = ""
    checkindate:str | None
    checkoutdate:str | None
    email: str
    first_name: str
    guestlist: List[Guest]
    last_name: str
    locale:str | None
    lodging:str | None
    meals:str | None
    mobile: str
    organizers:bool | None
    remarks:str | None = ""


class LodgingList(BaseModel):
    reservations: List[Any]

class DbLodging(DbBase):
    COLLECTION = "by_lodging"
    VERSION = 1
    IDGENERATOR = "uuid"
