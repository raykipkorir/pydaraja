"""This module contains daraja API services"""

import base64
import logging
import time
from datetime import datetime

import requests
from requests import ConnectionError, Response

from .exceptions import InvalidUrlError
from .utils import (
    _format_phone_number,
    _handle_access_token_response_errors,
    _handle_common_response_errors,
    _validate_amount,
    _validate_phone_number,
    authorize,
    retry_policy,
)

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class MpesaPaymentGateway:
    """Mpesa payment gateway."""

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        business_shortcode: str,
        passkey: str,
        endpoint: str,
    ) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.business_shortcode = business_shortcode
        self.passkey = passkey
        self.endpoint = endpoint
        self._access_token_url = (
            f"{self.endpoint}/oauth/v1/generate?grant_type=client_credentials"
        )
        self._stk_push_url = f"{self.endpoint}/mpesa/stkpush/v1/processrequest"
        self._query_stk_push_url = f"{self.endpoint}/mpesa/stkpushquery/v1/query"  # noqa: E501
        self._access_token_expiration_time = time.time()
        self._access_token = self._get_access_token()

    def _get_access_token(self) -> str:
        """Generate an OAuth access token."""
        if self._access_token_expiration_time < time.time():
            LOGGER.info(f"Mpesa API Token request: {self._access_token_url}")
            try:
                response = requests.get(
                    self._access_token_url,
                    auth=(self.consumer_key, self.consumer_secret),
                    timeout=30,
                )
            except ConnectionError:
                msg = "Provide a valid Daraja API endpoint."
                raise InvalidUrlError(msg)
            access_token = _handle_access_token_response_errors(self, response)
        else:
            access_token = self._access_token

        return access_token

    @retry_policy()
    @authorize
    def _make_request(self, *args, **kwargs) -> Response:
        kwargs["headers"] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._access_token}",
        }
        LOGGER.info(f"Mpesa API request: {kwargs['url']}")
        response = requests.post(*args, **kwargs, timeout=30)
        _handle_common_response_errors(response)
        return response

    def _generate_password(self):
        """Generates api password using the provided shortcode and passkey."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password_str = self.business_shortcode + self.passkey + timestamp
        password_bytes = password_str.encode("ascii")
        return base64.b64encode(password_bytes).decode("utf-8")

    def trigger_stk_push(
        self,
        phone_number: str,
        amount: int,
        callback_url: str,
        account_reference: str | None = None,
        transaction_desc: str | None = None,
    ):
        """Initiate a stk push prompt payment.

        :param phone_number: Provide valid phone number
        :param amount: Amount to be sent. Must be greater than 0
        :param callback_url: Callback url
        """
        _validate_phone_number(phone_number)
        phone_number = _format_phone_number(phone_number)
        _validate_amount(amount)
        if account_reference is None:
            account_reference = "Pydaraja"
        if transaction_desc is None:
            transaction_desc = "Python wrapper for mpesa api."
        headers = {}
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": self._generate_password(),
            "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc,
        }
        return self._make_request(url=self._stk_push_url, headers=headers, json=payload)  # noqa: E501

    def query_stk_push(self, checkout_request_id: str):
        """
        Query the status of stk push prompt payment.

        :param checkout_request_id: Acquired from the result of successful STK push payment # noqa: E501
        """
        headers = {}
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": self._generate_password(),
            "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
            "CheckoutRequestID": checkout_request_id,
        }
        return self._make_request(
            url=self._query_stk_push_url, headers=headers, json=payload
        )
