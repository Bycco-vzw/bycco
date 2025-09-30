# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from pydantic import BaseModel
from reddevil.core import DbBase


class RoomDB(BaseModel):
    """
    the room model as used in the database
    is normally not exposed in the API
    """

    blocked: bool  # blocked by organizer
    capacity: int
    enabled: bool
    number: str
    reservation_id: str
    reservation_nr: int
    roomtype: str
    _id: str
    _version: int
    _documenttype: str
    _creationtime: datetime
    _modificationtime: datetime


class Room(BaseModel):
    """
    the generic room model used in the application
    """

    blocked: bool | None = None
    capacity: int | None = None
    enabled: bool | None = None
    id: str | None = None
    number: str | None = None
    reservation_id: str | None = None
    reservation_nr: int | None = None
    roomtype: str | None = None
    _id: str | None = None
    _version: int | None = None
    _documenttype: str | None = None
    _creationtime: datetime | None = None
    _modificationtime: datetime | None = None


class RoomItem(BaseModel):
    """
    model used for lists of rooms
    """

    id: str | None = None
    number: str | None = None
    roomtype: str | None = None
    reservation_id: str | None = None
    reservation_nr: int | None = None


class DbRoom(DbBase):
    COLLECTION = "room"
    DOCUMENTTYPE = "Room"
    VERSION = 1
