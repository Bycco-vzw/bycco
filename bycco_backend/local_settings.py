COLORLOG = True

EMAIL = {
    "backend": "SMTP",
    "host": "maildev.decrop.net",
    "port": "1025",
    "sender": "noreply@bycco.be",
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
}

SECRETS_PATH = "/home/ruben/develop/secrets/bycco"