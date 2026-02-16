# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from jinja2 import PackageLoader, Environment
import pathlib
import csv

from bycco.participant import (
    ParticipantCategory,
    DbParticipant,
)

logger = logging.getLogger(__name__)
tmpl_env = Environment(loader=PackageLoader("bycco"), trim_blocks=True)
ROOTDIR = pathlib.Path(__file__).parents[3]


async def add_guest(
    first_name: str, last_name: str, category: ParticipantCategory
) -> None:
    """
    create a participant
    """
    logger.info("Adding guest")
    return await DbParticipant.add(
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


async def read_csv() -> None:
    """
    read_csv
    """
    logger.info(f"Rootdir: {ROOTDIR}")
    filepath = ROOTDIR / "share" / "data" / "eters2026.csv"
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for line in reader:
            last_name, first_name = line["name"].split(",")
            await add_guest(
                first_name=first_name,
                last_name=last_name,
                category=ParticipantCategory.GUEST,
            )
