# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import os
import logging
import io, csv
from typing import cast, List

from .md_room import DbRoom, Room, RoomItem
from bycco.core.common import load_common
from reddevil.core import RdBadRequest, get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
common = None
roomtypes = None


async def setup_globals():
    global common, roomtypes
    if not common:
        common = await load_common()
        roomtypes = [r["name"] for r in common["rooms"]]


async def get_room(id: str, options: dict = {}) -> Room:
    """
    get the Room
    """
    filter = options.copy()
    filter["id"] = id
    filter["_model"] = filter.pop("_model", Room)
    return cast(Room, await DbRoom.find_single(filter))


async def get_room_by_number(number: str, options: dict = {}) -> Room:
    """
    get room by number
    """
    filter = options.copy()
    filter["number"] = number
    filter["_model"] = filter.pop("_model", Room)
    return cast(Room, await DbRoom.find_single(filter))


async def get_rooms(options: dict = {}) -> List[RoomItem]:
    """
    get all Rooms
    """
    filter = options.copy()
    filter["_model"] = filter.pop("_model", RoomItem)
    if "_fieldlist" not in filter and filter["_model"] != RoomItem:
        filter["_fieldlist"] = filter["_model"].model_fields.keys()
    return [x for x in await DbRoom.find_multiple(filter)]


async def update_room(id: str, ru: Room, options: dict = {}) -> Room:
    """
    update a room
    """
    opt = options.copy()
    opt["_model"] = opt.pop("_model", Room)
    ur = cast(Room, await DbRoom.update(id, ru.model_dump(exclude_unset=True), opt))
    return ur


async def get_free_rooms(roomtype: str) -> List[RoomItem]:
    """
    get list of free rooms
    """
    await setup_globals()
    if roomtype not in roomtypes:
        logger.error(f"Unknown roomtype {roomtype}")
        raise RdBadRequest()
    rooms = await get_rooms(
        {
            "roomtype": roomtype,
            "blocked": False,
            "enabled": True,
            "reservation_id": None,
            "_model": RoomItem,
        }
    )
    return rooms


async def get_csv_rooms() -> str:
    """
    get all rooms in csv format
    """
    fieldnames = list(Room.model_fields.keys())
    csvstr = io.StringIO()
    csvf = csv.DictWriter(csvstr, fieldnames)
    csvf.writeheader()
    rooms = await get_rooms({"_model": Room})
    for room in rooms:
        csvf.writerow(room.model_dump())
    return csvstr.getvalue()


async def roominit(pathname: str) -> None:
    """
    get all rooms in csv format
    """
    logger.info(f"reading room from {pathname} {os.getcwd()}")
    with open(f"{settings.SHARED_PATH}/data/{pathname}") as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
            await DbRoom.add(
                {
                    "blocked": False,
                    "capacity": row["capacity"],
                    "enabled": True,
                    "number": row["roomnr"],
                    "roomtype": row["roomtype"],
                }
            )
