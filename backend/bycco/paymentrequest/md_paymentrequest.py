# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from datetime import datetime
from typing import Dict, Any, List, Optional, Type, Union
from enum import Enum
from pydantic import BaseModel, Field
from reddevil.core import DbBase


class PaymentDetail(BaseModel):
    description: str | None = None
    quantity: Any | None = None
    unitprice: str | None = None  # a Decimal
    totalprice: str | None = None  # a Decimal


class PaymentRequestDB:
    """
    as written in the database, for documentation purpose only
    """

    address: str
    checkindate: str  # format YYYY-MM-DD
    checkoutdate: str  # format YYYY-MM-DD
    details: List[PaymentDetail]
    email: str
    first_name: str
    guests: str
    idbel: str
    idfide: str
    last_name: str
    link_id: str
    locale: str
    mobile: str
    number: int
    paydate: str
    paymessage: str
    paystatus: bool
    reductionamount: str
    reductionpct: str
    remarks: str
    reason: str
    totalprice: str
    totalwithdiscount: str
    sentdate: str
    _creationtime: datetime
    _documenttype: str
    _id: str
    _modificationtime: datetime
    _version: int


class PaymentRequest(BaseModel):
    """
    base for all paymentRequest
    """

    address: str | None = None
    checkindate: str | None = None  # format YYYY-MM-DD
    checkoutdate: str | None = None  # format YYYY-MM-DD
    details: Optional[List[PaymentDetail]]
    email: str | None = None  # csl of email addresses
    first_name: str | None = None
    guests: str | None = None  # csl of firstname lastname
    id: str | None = None
    idbel: str | None = None
    idfide: str | None = None
    last_name: str | None = None
    link_id: str | None = None
    locale: str | None = None
    mobile: str | None = None
    number: int | None = None
    reductionamount: str | None = None
    reductionpct: str | None = None
    remarks: str | None = None
    paydate: str | None = None  # format YYYY-MM-DD
    paymessage: str | None = None  # '+++NNN-NNNN-NNNNN+++'
    paystatus: bool | None = None
    reason: str | None = None  # 'lodging' or 'enrollment'
    totalprice: str | None = None  # a Decimal
    totalwithdiscount: str | None = None  # a Decimal
    sentdate: str | None = None  # format YYYY-MM-DD
    _version: int | None = None
    _documenttype: str | None = None
    creationtime: datetime | None = None
    modificationtime: datetime | None = None


class PaymentRequestItem(BaseModel):
    """
    validator for list of paymentrequest( lodging and enrollment)
    """

    email: str
    first_name: str
    id: str
    idbel: str | None = ""
    idfide: str | None = ""
    locale: str
    last_name: str
    reductionamount: str | None = None
    reductionpct: str | None = None
    remarks: str | None = ""
    room: str | None = ""
    sentdate: str | None = None
    paydate: str | None = None
    paymessage: str | None = None
    paynumber: int | None = None
    price: dict
    enrollment_id: str | None = None
    enrollment_date: str | None = None
    creationtime: datetime | None = None
    modificationtime: datetime | None = None


class PaymentRequestUpdate(BaseModel):
    """
    validator for updating a PaymentRequest
    """

    address: str | None = None
    assignmentdate: str | None = None
    checkindate: str | None = None  # format YYYY-MM-DD
    checkoutdate: str | None = None  # format YYYY-MM-DD
    email: str | None = None  # comma separated list of email addresses
    first_name: str | None = None
    locale: str | None = None
    lodging_assigned: str | None = None
    lodging_requested: str | None = None
    last_name: str | None = None
    mobile: str | None = None
    reductionamount: str | None = None
    reductionpct: str | None = None
    remarks: str | None = None
    lodging_id: str | None = None
    room: str | None = None
    sentdate: str | None = None  # format YYY-MM-DD
    paydate: str | None = None  # format YYY-MM-DD
    paymessage: str | None = None  # structured message in '+++NNN-NNNN-NNNNN+++'
    paynumber: int | None = None  #
    paystatus: bool | None = None
    price: dict | None = None
    enrollment_date: str | None = None
    enrollment_id: str | None = None


class DbPayrequest(DbBase):
    COLLECTION = "by_paymentrequest"
    DOCUMENTTYPE = "Payrequest"
    VERSION = 1
    IDGENERATOR = "uuid"
