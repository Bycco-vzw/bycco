# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from jinja2 import PackageLoader, Environment


from bycco.participant import (
    ParticipantBJKCategory,
    DbParticpantBJK,
)

logger = logging.getLogger(__name__)
tmpl_env = Environment(loader=PackageLoader("bycco"), trim_blocks=True)


async def add_guest(
    first_name: str, last_name: str, category: ParticipantBJKCategory
) -> None:
    """
    create a participant
    """
    logger.info("Adding guest")
    return await DbParticpantBJK.add(
        {
            "badgemimetype": "",
            "badglength": 0,
            "badgeimage": None,
            "birthyear": 0,
            "category": category,
            "chesstitle": "",
            "enabled": True,
            "emails": [],
            "first_name": first_name,
            "gender": "M",
            "idbel": "",
            "idclub": "",
            "idfide": "",
            "locale": "nl",
            "last_name": last_name,
            "nationalityfide": "BEL",
            "ratingbel": 0,
            "ratingfide": 0,
            "remarks": "guest, arb or org",
        }
    )
