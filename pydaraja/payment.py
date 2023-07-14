"""This module contains daraja API services"""

__all__ = [
    "trigger_stk_push",
    "query_stk_push",
    "transaction_status",
    "account_balance",
]

from datetime import datetime

import requests
from requests import Response

from pydaraja import config
from pydaraja.utils import (
    _format_phone_number,
    _generate_access_token,
    _generate_password,
    _validate_amount,
    _validate_phone_number,
)


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
        "BusinessShortCode": config.BUSINESS_SHORTCODE,
        "Password": _generate_password(),
        "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": config.BUSINESS_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": config.CALLBACK_URL,
        "AccountReference": config.ACCOUNT_REFERENCE,
        "TransactionDesc": config.TRANSACTION_DESC,
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
        "BusinessShortCode": config.BUSINESS_SHORTCODE,
        "Password": _generate_password(),
        "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
        "CheckoutRequestID": checkout_request_id,
    }
    response = requests.post(url=url, headers=headers, json=payload, timeout=30)
    return response


def transaction_status(transaction_id: str) -> Response:
    """
    Check the status of a transanction

    :param transaction_id: Unique identifier to identify a transaction on Mpesa
    """
    url = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"
    payload = {
        "Initiator": config.INITIATOR,
        "SecurityCredential": config.SECURITY_CREDENTIAL,
        "CommandID": "TransactionStatusQuery",
        "TransactionID": transaction_id,
        "PartyA": config.PARTY_A,
        "IdentifierType": config.IDENTIFIER_TYPE,
        "ResultURL": config.RESULT_URL,
        "QueueTimeOutURL": config.QUEUE_TIMEOUT_URL,
        "Remarks": config.REMARKS,
        "Occasion": config.OCCASSION,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {_generate_access_token()}",
    }
    response = requests.post(url=url, json=payload, headers=headers, timeout=30)
    return response


def account_balance() -> Response:
    """
    Account Balance API is used to request the account balance of a short code
    """
    url = "https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query"
    payload = {
        "Initiator": config.INITIATOR,
        "SecurityCredential": config.SECURITY_CREDENTIAL,
        "CommandID": "AccountBalance",
        "PartyA": config.PARTY_A,
        "IdentifierType": config.IDENTIFIER_TYPE,
        "ResultURL": config.RESULT_URL,
        "QueueTimeOutURL": config.QUEUE_TIMEOUT_URL,
        "Remarks": config.REMARKS,
        "Occasion": config.OCCASSION,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {_generate_access_token()}",
    }
    response = requests.post(url=url, json=payload, headers=headers, timeout=30)
    return response
