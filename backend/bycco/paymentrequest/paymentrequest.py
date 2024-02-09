# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, Dict, Any, List
from datetime import date
from reddevil.core import get_settings
from reddevil.mail import sendEmailNoAttachments, MailParams

from . import PaymentRequest, PaymentRequestItem, DbPayrequest
from bycco.core.counter import DbCounter
from bycco.core.common import get_common
from bycco.lodging import get_lodging, update_lodging, Lodging

logger = logging.getLogger(__name__)

settings = get_settings()
common = get_common()
i18n = common["i18n"]
prices = common["prices"]
startdate = common["period"]["startdate"]
enddate = common["period"]["enddate"]
m3y = date(startdate.year - 3, startdate.month, startdate.day)
m12y = date(startdate.year - 12, startdate.month, startdate.day)
m18y = date(startdate.year - 18, startdate.month, startdate.day)

# crud


async def create_payment_request(d: Dict[str, Any] = {}) -> str:
    """
    create paymentrequest
    """
    id = await DbPayrequest.add(d)
    return id


async def delete_payment_request(id: str) -> None:
    """
    update paymentrequest
    """
    await DbPayrequest.delete(id)


async def get_payment_request(id: str, options: Dict[str, Any] = {}) -> PaymentRequest:
    """
    get paymentrequest
    """
    filter = options.copy()
    filter["id"] = id
    filter["_model"] = filter.pop("_model", PaymentRequest)
    return cast(PaymentRequest, await DbPayrequest.find_single(filter))


async def get_payment_requests(
    options: Dict[str, Any] = {}
) -> List[PaymentRequestItem]:
    """
    get paymentrequests
    """
    filter = options.copy()
    filter["_model"] = filter.pop("_model", PaymentRequest)
    if "_fieldlist" not in filter and filter["_model"] != PaymentRequest:
        filter["_fieldlist"] = filter["_model"].__fields__.keys()
    return [cast(PaymentRequest, pr) for pr in await DbPayrequest.find_multiple(filter)]


async def update_payment_request(id: str, pr: PaymentRequest, options={}) -> None:
    """
    update paymentrequest
    """
    opt = options.copy()
    pd = pr.model_dump(exclude_unset=True)
    opt["_model"] = opt.get("_model", PaymentRequest)
    return await DbPayrequest.update(id, pd, opt)


# app routines


def getPaymessage(n) -> str:
    p1, rm = divmod(n, 10000000)
    p2, p3 = divmod(rm, 1000)
    p4 = n % 97 or 97
    return f"+++{p1:03d}/{p2:04d}/{p3:03d}{p4:02d}+++"


def calc_pricedetails(
    rsv: Lodging,
    reductionamount: str | None = None,
    reductionpct: str | None = None,
):
    """
    calculates prices and details list
    """
    assert rsv.assignments and rsv.checkindate and rsv.checkoutdate
    assert rsv.guestlist

    details = []
    totalprice = 0.0
    checkroom18 = False
    ndays = int(rsv.checkoutdate[8:10]) - int(rsv.checkindate[8:10])
    logger.info(f"prices {prices}")
    for ass in rsv.assignments:
        details.append(
            {
                "description": i18n[ass.roomtype][rsv.locale],
                "quantity": ndays,
                "unitprice": format(prices[ass.roomtype]["day"], ">6.2f"),
                "totalprice": format(prices[ass.roomtype]["day"] * ndays, ">6.2f"),
            }
        )
        totalprice += prices[ass.roomtype]["day"] * ndays
        if ass.roomtype in ["SH", "DH", "TH"]:
            checkroom18 = True
        else:
            details.append(
                {
                    "description": i18n["cleaning"][rsv.locale],
                    "quantity": 1,
                    "unitprice": format(prices[ass.roomtype]["clean"], ">6.2f"),
                    "totalprice": format(prices[ass.roomtype]["clean"], ">6.2f"),
                }
            )
            totalprice += prices[ass.roomtype]["clean"]
    if checkroom18:
        for g in rsv.guestlist:
            assert g.birthdate
            bd = date.fromisoformat(g.birthdate)
            if bd > m18y:
                details.append(
                    {
                        "description": i18n["ROOM_18"][rsv.locale],
                        "quantity": ndays,
                        "unitprice": format(prices["ROOM_18"]["day"], ">6.2f"),
                        "totalprice": format(prices["ROOM_18"]["day"] * ndays, ">6.2f"),
                    }
                )
                totalprice += prices["ROOM_18"]["day"] * ndays
    if rsv.meals != "no":
        for g in rsv.guestlist:
            assert g.birthdate
            bd = date.fromisoformat(g.birthdate)
            age = "+18"
            if bd > m18y:
                age = "-18"
            if bd > m12y:
                age = "-12"
            if bd > m3y:
                age = "-3"
            details.append(
                {
                    "description": f"{g.first_name} {g.last_name} {i18n[rsv.meals][rsv.locale]}",
                    "quantity": ndays,
                    "unitprice": format(prices[age][rsv.meals], ">6.2f"),
                    "totalprice": format(prices[age][rsv.meals] * ndays, ">6.2f"),
                }
            )
            totalprice += prices[age][rsv.meals] * ndays
    details.append(
        {
            "description": f"{i18n['tax'][rsv.locale]} ( {len(rsv.guestlist)} Pers.)",
            "quantity": ndays * len(rsv.guestlist),
            "unitprice": format(2, ">6.2f"),
            "totalprice": format(2 * ndays * len(rsv.guestlist), ">6.2f"),
        }
    )
    totalprice += 2 * ndays * len(rsv.guestlist)
    if reductionamount or reductionpct:
        details.append(
            {
                "description": f"{i18n['costnor'][rsv.locale]}",
                "quantity": None,
                "unitprice": None,
                "totalprice": format(totalprice, ">6.2f"),
            }
        )
        if reductionamount:
            reduction = -float(reductionamount)
        else:
            assert reductionpct
            reduction = -(totalprice * float(reductionpct) / 100)
        details.append(
            {
                "description": f"{i18n['reduction'][rsv.locale]}",
                "quantity": None,
                "unitprice": None,
                "totalprice": format(reduction, ">6.2f"),
            }
        )
        totalprice += reduction
    details.append(
        {
            "description": f"{i18n['total'][rsv.locale]}",
            "quantity": None,
            "unitprice": None,
            "totalprice": format(totalprice, ">6.2f"),
        }
    )
    return (details, totalprice)


async def create_pr_lodging(rsvid: str) -> str:

    rsv = await get_lodging(rsvid)
    assert rsv.guestlist
    pr: Dict[str, Any] = {
        "address": rsv.address,
        "checkindate": rsv.checkindate,
        "checkoutdate": rsv.checkoutdate,
        "email": rsv.email,
        "first_name": rsv.first_name,
        "last_name": rsv.last_name,
        "link_id": rsvid,
        "locale": rsv.locale,
        "mobile": rsv.mobile,
        "paystatus": False,
        "reason": "lodging",
    }
    pr["details"], pr["totalprice"] = calc_pricedetails(rsv)
    pr["number"] = await DbCounter.next("paymentrequest")
    pr["paymessage"] = getPaymessage(20240000 + pr["number"])
    pr["guests"] = ", ".join([f"{g.first_name} {g.last_name}" for g in rsv.guestlist])
    id = await create_payment_request(pr)
    await update_lodging(rsvid, Lodging(payment_id=id))
    return id


async def delete_pr_lodging(rsvid: str) -> None:
    from bycco.lodging import get_lodging, update_lodging

    rsv = await get_lodging(rsvid)
    payment_id = rsv.payment_id
    assert payment_id
    await update_lodging(rsvid, Lodging(payment_id=None))
    try:
        await delete_payment_request(payment_id)
    except:
        logger.info("Could not delete linked payment request")
        pass


async def update_pr_lodging(id: str, prq: PaymentRequest) -> None:
    prq = await get_payment_request(id)
    assert prq.reason == "lodging"
    rsv = await get_lodging(prq.link_id)
    (details, totalprice) = calc_pricedetails(
        rsv, prq.reductionamount, prq.reductionpct
    )
    prq.details = details
    prq.totalprice = totalprice
    await update_payment_request(id, prq)


async def email_paymentrequest(prqid) -> None:
    prq = await get_payment_request(prqid)
    if prq.reason == "enrollment":
        await email_pr_enrollment(prqid)
    else:
        await email_pr_lodging(prqid)


async def email_pr_lodging(prqid) -> None:
    prq = await get_payment_request(prqid)
    assert prq.email and prq.locale
    mp = MailParams(
        subject="Floreal 2023",
        sender=settings.EMAIL["sender"],
        receiver=prq.email,
        template="pr_lodging_mail_{locale}.md",
        locale=prq.locale,
        attachments=[],
        bcc=settings.EMAIL["bcc_reservation"],
    )
    sendEmailNoAttachments(mp, prq.model_dump(), "payment request lodging")
    await update_payment_request(
        prqid, PaymentRequest(sentdate=date.today().isoformat())
    )


def calc_enrollment(
    enr: Lodging,
    reductionamount: str | None = None,
    reductionpct: str | None = None,
):
    """
    calculates cost for enrollment
    """
    ## TODO


async def create_pr_enrollment(enrid: str, admincost: str = "#NA") -> str:
    from bycco.service.enrollment import get_enrollment, update_enrollment

    enr = await get_enrollment(enrid)
    assert enr.registrationtime
    emails = []
    for em in [enr.emailplayer, enr.emailparent, enr.emailattendant]:
        if em:
            emails.append(em)
    pr: Dict[str, Any] = {
        "email": ",".join(emails),
        "first_name": enr.first_name,
        "last_name": enr.last_name,
        "link_id": enrid,
        "locale": enr.locale,
        "mobile": enr.mobileparent or enr.mobileplayer,
        "paystatus": False,
        "reason": "enrollment",
    }
    d = [
        {
            "description": f"{i18n['enrollment'][enr.locale]} {enr.first_name} {enr.last_name}",
            "quantity": 1,
            "unitprice": format(35, ">6.2f"),
            "totalprice": format(35, ">6.2f"),
        }
    ]
    t = 35
    if admincost == "#NA":
        addadmincost = enr.registrationtime > finalday
    else:
        addadmincost = admincost == "1"
    logger.info(f"admincost {admincost},  addadmincost {addadmincost}")
    if addadmincost:
        d.append(
            {
                "description": f"{i18n['admcost'][enr.locale]}",
                "quantity": 1,
                "unitprice": "",
                "totalprice": format(10, ">6.2f"),
            }
        )
        t = 45
    d.append(
        {
            "description": f"{i18n['total'][enr.locale]}",
            "quantity": None,
            "unitprice": None,
            "totalprice": format(t, ">6.2f"),
        }
    )
    pr["details"] = d
    pr["totalprice"] = t
    pr["number"] = await DbCounter.next("paymentrequest")
    pr["paymessage"] = getPaymessage(20230000 + pr["number"])
    id = await create_payment_request(pr)
    await update_enrollment(enrid, EnrollmentUpdate(payment_id=id))
    return id


async def delete_pr_enrollment(enrid: str) -> None:
    from bycco.service.enrollment import get_enrollment, update_enrollment

    enr = await get_enrollment(enrid)
    payment_id = enr.payment_id
    assert payment_id
    await update_enrollment(enrid, EnrollmentUpdate(payment_id=None))
    try:
        await delete_payment_request(payment_id)
    except:
        logger.info("Could not delete payment request")
        pass


async def update_pr_enrollment(enrid: str, prq: PaymentRequest) -> None:
    from bycco.service.enrollment import get_enrollment

    enr = await get_enrollment(enrid)
    ## TODO
    # (details, totalprice) = calc_pricedetails(
    #     enr, prq.reductionamount, prq.reductionpct
    # )
    # prq.details = details
    # prq.totalprice = totalprice
    assert enr.payment_id
    await update_payment_request(enr.payment_id, prq)


async def email_pr_enrollment(prqid: str) -> None:
    from bycco.service.enrollment import get_enrollment

    prq = await get_payment_request(prqid)
    assert prq.link_id
    enr = await get_enrollment(prq.link_id)
    assert enr.registrationtime
    emails = []
    for em in [enr.emailplayer, enr.emailparent, enr.emailattendant]:
        if em:
            emails.append(em)
    assert prq.email and prq.locale
    mp = MailParams(
        subject="BJK - CBJ - BJLM - BYCC  2023",
        sender=settings.EMAIL["sender"],
        receiver=",".join(emails),
        template="mailpayenroll_{locale}.md",
        locale=prq.locale,
        attachments=[],
        bcc=settings.EMAIL["bcc_enrollment"],
    )
    sendEmailNoAttachments(mp, prq.dict(), "payment request enrollment")
    await update_payment_request(
        prqid, PaymentRequest(sentdate=date.today().isoformat())
    )
