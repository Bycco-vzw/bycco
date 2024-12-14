COLORLOG = True

EMAIL = {
    "backend": "SMTP",
    "host": "maildev.decrop.net",
    "port": "1025",
    "sender": "noreply@bycco.be",
    "bcc_reservation": "ruben.decrop@gmail.com,floreal@bycco.be",
    "bcc_registration": "ruben.decrop@gmail.com,luc.cornet@bycco.be",
}


SECRETS = {
    "mongodb": {
        "name": "bycco-mongodb-dev",
        "manager": "filejson",
    },
    "gmail": {
        "name": "bycco-gmail-prod",
        "manager": "filejson",
    },
    "statamic": {
        "name": "statamic-server",
        "manager": "filejson",
    },
}

TEMPLATES_PATH = "./backend/bycco/templates"
