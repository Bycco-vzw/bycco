#    Copyright 2019 Chessdevil Consulting

import logging
import os
import smtplib
import base64
from pathlib import Path
from fastapi import HTTPException
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.base import MIMEBase
from bycco.main import settings
from reddevil.core import get_secret

logger = logging.getLogger(__name__)
cwd = Path(".")


class BaseEmailBackend:
    def send_message(self, message: MIMEBase):
        raise HTTPException(503, detail="EmailBackendNotImplemented")


class SmtpSslBackend(BaseEmailBackend):
    def send_message(self, msg: MIMEBase):
        with smtplib.SMTP_SSL(settings.EMAIL["host"], settings.EMAIL["port"]) as s:
            if settings.EMAIL.get("user"):
                s.login(settings.EMAIL["user"], settings.EMAIL["password"])
            s.send_message(msg)


class SmtpBackend(BaseEmailBackend):
    def send_message(self, msg: MIMEBase):
        with smtplib.SMTP(settings.EMAIL["host"], settings.EMAIL["port"]) as s:
            if settings.EMAIL.get("user"):
                s.login(settings.EMAIL["user"], settings.EMAIL["password"])
            s.send_message(msg)


class GmailBackend(BaseEmailBackend):
    def send_message(self, msg: MIMEBase):
        service = get_gmail_service()
        rmsg = {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")}
        try:
            service.users().messages().send(userId="me", body=rmsg).execute()
        except Exception as e:
            logger.exception("sending Gmail message failed")


def get_gmail_service():
    if not hasattr(get_gmail_service, "service"):
        secret = get_secret("gmail")
        try:
            cr = service_account.Credentials.from_service_account_info(
                secret, scopes=["https://www.googleapis.com/auth/gmail.send"]
            )
            delegated_credentials = cr.with_subject(settings.EMAIL["account"])
            service = build("gmail", "v1", credentials=delegated_credentials)
            get_gmail_service.service = service
        except Exception:
            logger.exception("Cannot setup Gmail API")
            raise HTTPException(503, detail="GmailAPINotAvailable")
    return get_gmail_service.service


backends = {
    "SMTP": SmtpBackend,
    "SMTP_SSL": SmtpSslBackend,
    "GMAIL": GmailBackend,
}
