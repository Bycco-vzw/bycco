# This file creates some test endpoint
# the endpoints are excluded from the api docs  (endpoint /docs)

import logging
from reddevil.core import get_settings
from bycco.main import app
from bycco.core.mail import test_mail


logger = logging.getLogger(__name__)
settings = get_settings()


# this endpoint is useful to test if the server is running and accepting http requests
@app.get("/api/hello", include_in_schema=False)
def hello():
    return "hello world"


@app.get("/api/testmail", include_in_schema=False)
def api_test_mail():
    test_mail()
    return "Mail sent"
