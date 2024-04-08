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

env = Environment(loader=FileSystemLoader("bycco/templates"), trim_blocks=True)

logger = logging.getLogger(__name__)

# vk


async def add_attendees_vk(att: Attendee) -> str:
    elem = att.model_dump(exclude_none=True)
    id = await DbAttendee.add(elem)
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


async def generate_badges_vk(filter: dict = {}):
    """
    get the badges for the vl
    """
    logger.info(f"filter {filter}")
    prts = await get_attendees_vk(filter)
    logger.info(f"nr of attendees {len(prts)}")
    pages = []
    badges = []
    j = 0
    sorteddocs = sorted(prts, key=lambda x: f"{x.last_name}, {x.first_name}")
    for ix, p in enumerate(sorteddocs):
        rix = j % 2 + 1
        cix = j // 2 + 1
        badge = {
            "first_name": p.first_name,
            "last_name": p.last_name,
            # "rating": max(p.ratingbel or 0, p.ratingfide or 0),
            "chesstitle": "",
            "category": p.category.value,
            # "meals": p.meals or "",
            # "mealsclass": "badge_{}".format(p.meals or "NM"),
            # "photourl": f"/photo/{p.id}",
            "positionclass": "badge{0}{1}".format(cix, rix),
            "ix": ix,
        }
        # log.info(f"badge: {badge}")
        badges.append(badge)
        j += 1
        if j == 8:
            j = 0
            pages.append(badges)
            badges = []
    if j > 0:
        pages.append(badges)
    tmpl = env.get_template("printbadge_vk.j2")
    return tmpl.render({"pages": pages})
