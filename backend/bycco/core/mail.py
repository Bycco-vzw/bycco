# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from markdown2 import Markdown
from jinja2 import FileSystemLoader, Environment
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
from pathlib import Path
from weasyprint import HTML, CSS
from reddevil.core import get_settings
from reddevil.mail.md_mail import MailParams

from bycco.lodging.md_lodging import Lodging
from bycco.core.mailbackend import backends
from bycco.core.common import get_common

logger = logging.getLogger(__name__)
settings = get_settings()
md = Markdown(extras=["tables"])
env = Environment(loader=FileSystemLoader(settings.TEMPLATES_PATH), trim_blocks=True)
common = get_common()
i18n = common["i18n"]


markdownstyle = """
<style>
th, td {
    padding: 8px;
    border: 1px solid #ddd;
}

table {
    border-collapse: collapse;
}

h1:after {
    content: ' ';
    display: block;
    border: 1px solid #aaa;
    margin-bottom: 1em;
}

ul, ol, h2, h3 {
    margin-bottom: 0.5em;
}
</style>
"""


def getCss():
    if not hasattr(getCss, "css"):
        with open(Path(settings.TEMPLATES_PATH) / "markdown.css") as f:
            setattr(getCss, "css", f.read())
    return getattr(getCss, "css")


def test_mail():
    """
    send a test mail
    """
    logger.info("sending testmail email")
    try:
        sender = settings.EMAIL["sender"]
        receiver = "ruben.decrop@gmail.com"
        msg = MIMEMultipart("related")
        msg["Subject"] = "Testmail 2"
        msg["From"] = sender
        msg["To"] = receiver
        msg.preamble = "This is a multi-part message in MIME format."
        msgAlternative = MIMEMultipart("alternative")
        msgText = MIMEText("Hi it is I Leclercq, I am in disguise")
        msgAlternative.attach(msgText)
        msgText = MIMEText("Hi, It is I <b>Leclercq</b> I am in disguise", "html")
        msgAlternative.attach(msgText)
        msg.attach(msgAlternative)
        mailbackend = backends[settings.EMAIL["backend"]]()
        mailbackend.send_message(msg)
        logger.info(f"testmail sent for {receiver}")
    except Exception:
        logger.exception("failed")


def sendemail_reservation(ldg: Lodging):
    logger.info(f"sending reservation email {ldg}")
    tmpl = env.get_template(f"mailreservation_{ldg.locale}.md")
    context = ldg.model_dump()
    # translate
    context["lodging"] = i18n[context["lodging"]][context["locale"]]
    context["meals"] = i18n[context["meals"]][context["locale"]]
    # render the content using jinja2 templating giving markdown text
    markdowntext = tmpl.render(**context)
    # convert markdown text to html
    htmltext = f"{markdownstyle} {md.convert(markdowntext)}"
    try:
        sender = settings.EMAIL["sender"]
        receiver = ldg.email
        msg = MIMEMultipart("related")
        msg["Subject"] = "Floreal 2023"
        msg["From"] = sender
        msg["To"] = receiver
        if settings.EMAIL.get("bcc_reservation"):
            msg["Bcc"] = settings.EMAIL["bcc_reservation"]
        msg.preamble = "This is a multi-part message in MIME format."
        msgAlternative = MIMEMultipart("alternative")
        msgText = MIMEText(markdowntext)
        msgAlternative.attach(msgText)
        msgText = MIMEText(htmltext, "html")
        msgAlternative.attach(msgText)
        msg.attach(msgAlternative)
        backend = backends[settings.EMAIL["backend"]]()
        backend.send_message(msg)
        logger.info(f"reservation email sent to {receiver}")
    except Exception:
        logger.exception("failed")


def sendemail_no_attachments(mp: MailParams, context: dict, name: str = ""):
    tmpl = env.get_template(mp.template.format(locale=context["locale"]))
    markdowntext = tmpl.render(**context)
    htmltext = f"{markdownstyle} {md.convert(markdowntext)}"
    try:
        msg = MIMEMultipart("related")
        msg["Subject"] = mp.subject
        msg["From"] = mp.sender
        msg["To"] = mp.receiver
        if mp.bcc:
            msg["Bcc"] = mp.bcc
        msg.preamble = "This is a multi-part message in MIME format."
        msgAlternative = MIMEMultipart("alternative")
        msgText = MIMEText(markdowntext)
        msgAlternative.attach(msgText)
        msgText = MIMEText(htmltext, "html")
        msgAlternative.attach(msgText)
        msg.attach(msgAlternative)
        backend = backends[settings.EMAIL["backend"]]()
        backend.send_message(msg)
        logger.info(f"email {name} sent to {mp.receiver}")
    except Exception:
        logger.exception("failed")
