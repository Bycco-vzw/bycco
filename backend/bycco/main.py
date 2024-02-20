# copyright Ruben Decrop 2012 - 2024
# copyright Chessdevil Consulting 2015 - 2024

import os.path
import logging, logging.config

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from reddevil.core import register_app, get_settings, connect_mongodb, close_mongodb

import mimetypes


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_mongodb()
    yield
    close_mongodb()


# load and register app
app = FastAPI(
    title="Bycco backend",
    description="backend website bycco.be",
    version="0",
    lifespan=lifespan,
)
load_dotenv()
register_app(app, "bycco.settings", "/api")
settings = get_settings()
logger = logging.getLogger(__name__)
logger.info(f"Starting website bycco ...")

# add CORS middleware for dev only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# import api endpoints
from reddevil.account import api_account
from reddevil.filestore import api_filestore
from bycco.lodging import api_lodging
from bycco.enrollment import api_enrollment
from bycco.room import api_room
from bycco.paymentrequest import api_paymentrequest

app.include_router(api_account.router)
app.include_router(api_enrollment.router)
app.include_router(api_filestore.router)
app.include_router(api_lodging.router)
app.include_router(api_room.router)
app.include_router(api_paymentrequest.router)


logger.info(f"Api layer loaded")

# fetch the common

#    Simplify operation IDs so that generated API clients have simpler function
#    names.
for route in app.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name[4:]

# importing test endpoints
import bycco.tst_endpoints
