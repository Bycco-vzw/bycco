# copyright Ruben Decrop 2012 - 2024
# copyright Chessdevil Consulting 2015 - 2024

import os.path
import logging, logging.config

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from reddevil.core import register_app, get_settings
from reddevil.filestore import api_filestore
import mimetypes


# load and register app
app = FastAPI(
    title="Bycco backend",
    description="backend website bycco.be",
    version="0",
)
register_app(app, "bycco.settings", "/api")

# get settings
settings = get_settings()
logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("bycco")
logger.info(f"Starting website reddevilmgr ...")

# show local settings loaded or not
from bycco.settings import ls

logger.info(ls)

# import api endpoints
app.include_router(api_filestore.router)
logger.info(f"Api layer loaded")

# add CORS middleware for dev only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#    Simplify operation IDs so that generated API clients have simpler function
#    names.
for route in app.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name[4:]

import  bycco.tst_endpoints
