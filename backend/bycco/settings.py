# Copyright 2022-2024 Chessdevil Consulting
# Copyright 2015-2024 Ruben Decrop

import os, os.path
import logging
from pathlib import Path

BYCCO_MODE = os.environ.get("BYCCO_MODE", "production")

COLORLOG = False

COMMON_PATH = "../content/common.yaml"

EMAIL = {
    "backend": os.environ.get("EMAIL_BACKEND", "GMAIL"),
    "sender": "ruben.decrop@bycco.be",
    "bcc_reservation": "ruben.decrop@gmail.com,floreal@bycco.be",
    "bcc_enrollment": "ruben.decrop@gmail.com,luc.cornet@bycco.be",
    # "gmail_file": os.environ.get("GMAIL_FILE", "chessdevil-gmail.json"),
    "account": "ruben.decrop@bycco.be",
}


FILESTORE = {
    "manager": "google",
    "bucket": os.environ.get("FILESTORE_BUCKET", "byccowebsiteprod.appspot.com"),
}

GOOGLE_CLIENT_ID = (
    "464711449307-7j2oecn3mkfs1eh3o7b5gh8np3ebhrdp.apps.googleusercontent.com"
)
GOOGLE_LOGIN_DOMAINS = ["bycco.be"]
GOOGLE_PROJECT_ID = "byccowebsiteprod"

JWT_ALGORITHM = "HS256"
JWT_SECRET = "levedetorrevanostende"

KBSB_HOST = "https://www.frbe-kbsb-ksb.be"

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(levelname)s: %(asctime)s %(name)s %(message)s",
        },
        "color": {
            "format": "%(log_color)s%(levelname)s%(reset)s: %(asctime)s %(bold)s%(name)s%(reset)s %(message)s",
            "()": "reddevil.core.colorlogfactory.c_factory",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "bycco": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "reddevil": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "fastapi": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

SECRETS = {
    "mongodb": {
        "name": "bycco-mongodb",
        "manager": "googlejson",
    },
    "gmail": {
        "name": "bycco-gmail",
        "manager": "googlejson",
    },
    "statamic": {
        "name": "statamic-server",
        "manager": "googlejson",
    },
}

SECRETS_PATH = Path(os.environ.get("SECRETS_PATH", ""))

SHARED_PATH = Path(os.environ.get("SHARED_PATH", "../share"))

TEMPLATES_PATH = Path(os.environ.get("TEMPLATES_PATH", "./bycco/templates"))

TOKEN = {
    "timeout": 180,  # timeout in minutes
    "secret": "kennehvrowe,endaklaagtendazaagt",
    "algorithm": "HS256",
    "nocheck": False,
}

ls = "No local settings found"

if BYCCO_MODE == "local":
    ls = "importing local settings"
    from env_local import *


if BYCCO_MODE == "prodtest":
    ls = "importing prodtest settings"
    from env_prodtest import *

if COLORLOG:
    LOG_CONFIG["handlers"]["console"]["formatter"] = "color"  # type: ignore

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)
logger.info(ls)
