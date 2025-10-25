import asyncio
import aiofiles
import aiocsv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from reddevil.core import (
    register_app,
    connect_mongodb,
    close_mongodb,
    get_settings,
)
from dotenv import load_dotenv
from bycco import ROOT_DIR
from bycco.room import RoomAdd, DbRoom, get_room_by_number
import logging


app = FastAPI(
    title="Bycco",
    description="Website Bycco",
    version="0",
)
load_dotenv()
register_app(app=app, settingsmodule="bycco.settings")
settings = get_settings()
logger = logging.getLogger("bycco")
logger.info("Started")


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_mongodb()
    yield
    close_mongodb()


async def main():
    print("ROOT_DIR:", ROOT_DIR)
    infile = ROOT_DIR / "share" / "data" / "rooms_adapted.csv"
    async with lifespan(app) as writer:  # noqa: F841
        async with aiofiles.open(
            infile, mode="r", encoding="utf-8", newline=""
        ) as reader:
            async for row in aiocsv.AsyncDictReader(reader):
                existing = await get_room_by_number(row["roomnumber"])
                if existing and existing.roomtype != row["roomtype"]:
                    await DbRoom.update(existing.id, {"roomtype": row["roomtype"]})

if __name__ == "__main__":
    asyncio.run(main())
