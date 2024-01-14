# Copyright 2022-2024 Chessdevil Consulting
# Copyright 2015-2024 Ruben Decrop

import os, os.path
from pathlib import Path

# paths
SECRETS_PATH = Path(os.environ.get("SECRETS_PATH", ""))

COLORLOG = False

EMAIL = {
    "backend": os.environ.get("EMAIL_BACKEND", "GMAIL"),
    "sender": "noreply@talistro.com",
    "bcc": "ruben.kbsb@gmail.com",
    "gmail_file": os.environ.get("GMAIL_FILE", "chessdevil-gmail.json"),
    "account": "ruben@chessdevil.net",
}


FILESTORE = {
    "manager": "google",
    "bucket": os.environ.get("FILESTORE_BUCKET", "byccowebsiteprod.appspot.com"),
}


GOOGLE_PROJECT_ID = "byccowebsiteprod"

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
}

TEMPLATES_PATH = Path(os.environ.get("TEMPLATES_PATH", "./bycco/templates"))


try:
    from local_settings import *

    ls = "local settings loaded"
except ImportError:
    ls = "No local settings found"

if COLORLOG:
    LOG_CONFIG["handlers"]["console"]["formatter"] = "color"  # type: ignore
