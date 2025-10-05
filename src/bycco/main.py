# copyright Ruben Decrop 2012 - 2024
# copyright Chessdevil Consulting 2015 - 2024

import logging
import logging.config

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from reddevil.core import register_app, get_settings, connect_mongodb, close_mongodb

# to support yaml/json mimetype
# import mimetypes


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_mongodb()
    yield
    close_mongodb()


from . import version  # noqa E402


# load and register app
app = FastAPI(
    title="Bycco backend",
    description="backend website bycco.be",
    version=version,
    lifespan=lifespan,
)
load_dotenv()
register_app(app, "bycco.settings", "/api")
settings = get_settings()
logger = logging.getLogger(__name__)
logger.info(f"Starting website bycco {version} ...")

# add CORS middleware for dev only
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://www.bycco.be",
        "*byccowebsiteprod.ew.r.appspot.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# import api endpoints
logger.info("loading api_account")
from reddevil.account import api_account  # noqa E402

logger.info("loading api_attendee")
from bycco.attendee import api_attendee  # noqa E402

logger.info("loading api_filestore")
from reddevil.filestore import api_filestore  # noqa E402

logger.info("loading api_stay")
from bycco.stay import api_stay  # noqa E402

logger.info("loading api_room")
from bycco.room import api_room  # noqa E402

logger.info("loading api_page")
from bycco.page import api_page  # noqa E402

logger.info("loading api_participant")
from bycco.participant import api_participant  # noqa E402

logger.info("loading api_paymentrequest")
from bycco.paymentrequest import api_paymentrequest  # noqa E402

logger.info("loading api_registration")
from bycco.registration import api_registration  # noqa E402

logger.info("loading api_statamic")
from bycco.statamic import api_statamic  # noqa E402

logger.info("loading api_tournament")
from bycco.tournament import api_tournament  # noqa E402

logger.info("loading api_guest")
from bycco.guest import api_guest  # noqa E402


app.include_router(api_account.router)
app.include_router(api_attendee.router)
app.include_router(api_filestore.router)
app.include_router(api_stay.router)
app.include_router(api_registration.router)
app.include_router(api_room.router)
app.include_router(api_participant.router)
app.include_router(api_paymentrequest.router)
app.include_router(api_statamic.router)
app.include_router(api_page.router)
app.include_router(api_tournament.router)
app.include_router(api_guest.router)
logger.info("Api's loaded")


# static files fro dev only
if settings.BYCCO_MODE != "production":
    app.mount("/css", StaticFiles(directory="frontend/public/css"), name="css")
    app.mount("/img", StaticFiles(directory="frontend/public/img"), name="img")
    logger.info("static dirs loaded")


#    Simplify operation IDs so that generated API clients have simpler function names.
for route in app.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name[4:]

logger.info("routes adapted")

# importing test endpoints
import bycco.tst_endpoints  # noqa E402

logger.info("test endpoints loaded")
