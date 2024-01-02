# This file creates some test endpoint
# the endpoints are excluded from the api docs  (endpoint /docs)

import logging
from fastapi import Depends
from reddevil.core import get_settings
from bycco.main import app


logger = logging.getLogger(__name__)
settings = get_settings()


# this endpoint is useful to test if the server is running and accepting http requests
@app.get("/api", include_in_schema=False)
def hello():
    return "hello world"

