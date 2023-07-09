"""This module contains utility functions"""

import base64
import re
from datetime import datetime

import requests

from pydaraja import payment


def _generate_access_token() -> str:
    """Generate an OAuth access token"""
    access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(
        access_token_url,
        auth=(payment.CONSUMER_KEY, payment.CONSUMER_SECRET),
        timeout=30,
    )
    access_token = response.json()["access_token"]
    return access_token


def _generate_password() -> str:
    """Generates mpesa api password using the provided shortcode and passkey"""

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password_str = payment.BUSINESS_SHORTCODE + payment.PASSKEY + timestamp
    password_bytes = password_str.encode("ascii")
    return base64.b64encode(password_bytes).decode("utf-8")


def _validate_phone_number(phone_number: str) -> None:
    """Validate phone number"""

    pattern = r"^(?:254|\+254|0)?((?:(?:7(?:(?:[01249][0-9])|(?:5[789])|(?:6[89])))|(?:1(?:[1][0-5])))[0-9]{6})$"

    assert re.match(pattern, phone_number), "Invalid phone number"


def _format_phone_number(phone_number: str) -> str:
    """Format phone number"""

    if phone_number.startswith("+"):
        return phone_number.strip("+")
    if phone_number.startswith("0"):
        return phone_number.replace("0", "254", 1)

    return phone_number


def _validate_amount(amount: int) -> None:
    assert amount > 0, "Amount must be greater than 0"
