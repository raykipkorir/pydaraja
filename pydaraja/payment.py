"""This module contains daraja API services"""

__all__ = ["trigger_stk_push", "query_stk_push"]

from datetime import datetime

import requests
from requests import Response

from pydaraja.utils import (
    _format_phone_number,
    _generate_access_token,
    _generate_password,
    _validate_amount,
    _validate_phone_number,
)

BUSINESS_SHORTCODE: str = ""
PASSKEY: str = ""
CONSUMER_SECRET: str = ""
CONSUMER_KEY: str = ""
CALLBACK_URL: str = ""
ACCOUNT_REFERENCE: str = "Pydaraja"
TRANSACTION_DESC: str = "Python wrapper for mpesa api"


def trigger_stk_push(phone_number: str, amount: int) -> Response:
    """
    Initiate a stk push prompt payment
    :param phone_number: Provide valid phone number
    :param amount: Amount to be sent. Must be greater than 0
    """
    _validate_phone_number(phone_number)
    phone_number = _format_phone_number(phone_number)
    _validate_amount(amount)
    stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": _generate_password(),
        "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": ACCOUNT_REFERENCE,
        "TransactionDesc": TRANSACTION_DESC,
    }
    headers = {"Authorization": f"Bearer {_generate_access_token()}"}
    reponse = requests.post(url=stk_push_url, headers=headers, json=payload, timeout=30)
    return reponse


def query_stk_push(checkout_request_id: str) -> Response:
    """
    Query the status of stk push prompt payment
    :param checkout_request_id: Acquired from the result of successful STK push payment
    """
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {_generate_access_token()}",
    }
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": _generate_password(),
        "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "CheckoutRequestID": checkout_request_id,
    }
    response = requests.post(url=url, headers=headers, json=payload, timeout=30)
    return response
