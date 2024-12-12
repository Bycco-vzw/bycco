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
import logging


app = FastAPI(
    title="FRBE-KBSB-KSB",
    description="Website Belgian Chess federation FRBE KBSB KSB",
    version="0",
)
load_dotenv()
register_app(app=app, settingsmodule="kbsb.settings")
settings = get_settings()
logger = logging.getLogger("kbsb")
logger.info("Started")


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_mongodb()
    yield
    close_mongodb()


async def main():
    infile = ROOT_DIR / "share" / "data" / "icseries2425.csv"
    async with lifespan(app) as writer:
        async with aiofiles.open(
            infile, mode="r", encoding="utf-8", newline=""
        ) as reader:
            async for team in aiocsv.AsyncDictReader(reader):
                await script_addteam_icseries(
                    division=int(team.get("division")),
                    index=team.get("index"),
                    name=team.get("team"),
                    pairingnumber=team.get("pairingnr"),
                    idclub=team.get("idclub"),
                )


if __name__ == "__main__":
    asyncio.run(main())
