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
    cards = []
    j = 0
    sorteddocs = sorted(prts, key=lambda x: f"{x.last_name}, {x.first_name}")
    for ix, p in enumerate(sorteddocs):
        rix = j % 2 + 1
        ct = ""
        # ct = p.chesstitle + " " if p.chesstitle else ""
        card = {
            "fullname": "{0}{1} {2}".format(ct, p.last_name, p.first_name),
            "natrating": p.ratingbel or 0,
            "fiderating": p.ratingfide or 0,
            "category": p.category.value,
            "nationalityfide": p.nationalityfide,
            # 'photourl': '/photo/{0}'.format(p.id),
            "positionclass": "card_1{0}".format(rix),
            "ix": ix,
        }
        cards.append(card)
        j += 1
        if j == 2:
            j = 0
            pages.append(cards)
            cards = []
    if j > 0:
        pages.append(cards)
    tmpl = env.get_template("printnamecard_vk.j2")
    return tmpl.render({"pages": pages})
