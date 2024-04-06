# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, List, Dict, Any
from jinja2 import FileSystemLoader, Environment

from reddevil.core import RdBadRequest, RdNotFound
from bycco.attendee import (
    Attendee,
    AttendeeItem,
    AttendeeCategory,
    DbAttendee,
)

logger = logging.getLogger(__name__)

# vk


async def add_attendees_vk(adict: dict = {}) -> str:
    id = await DbAttendee.add(adict)
    return id


async def get_attendee_vk(id: str) -> Attendee:
    return await DbAttendee.find_single({"_model": Attendee, "id": id})


async def get_attendees_vk(options: dict = {}) -> List[AttendeeItem]:
    filter = options.copy()
    filter["_model"] = filter.pop("_model", AttendeeItem)
    return [cast(AttendeeItem, x) for x in await DbAttendee.find_multiple(filter)]


async def update_update_bjk(id: str, att: Attendee, options: dict = {}) -> Attendee:
    opt = options.copy()
    opt["_model"] = opt.pop("_model", Attendee)
    return cast(
        Attendee,
        await DbAttendee.update(id, att.model_dump(exclude_unset=True), opt),
    )
