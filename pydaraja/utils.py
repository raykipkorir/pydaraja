"""This module contains utility functions"""

import re
from functools import wraps


def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        self._access_token = self._get_access_token()
        response = func(*args, **kwargs)
        return response

    return wrapper


def _validate_phone_number(phone_number: str) -> None:
    """Validate phone number."""
    pattern = r"^(?:254|\+254|0)?((?:(?:7(?:(?:[01249][0-9])|(?:5[789])|(?:6[89])))|(?:1(?:[1][0-5])))[0-9]{6})$"  # noqa: E501

    assert re.match(pattern, phone_number), "Invalid phone number"


def _format_phone_number(phone_number: str) -> str:
    """Format phone number."""
    if phone_number.startswith("+"):
        return phone_number.strip("+")
    if phone_number.startswith("0"):
        return phone_number.replace("0", "254", 1)

    return phone_number


def _validate_amount(amount: int) -> None:
    """Validate payment amount."""
    assert amount > 0, "Amount must be greater than 0"
