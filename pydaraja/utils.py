"""This module contains utility functions"""

import inspect
import logging
import random
import re
import time
from functools import wraps

from requests import Response

from .constants import CLIENT_ERROR_CODES, IDEMPOTENCY_ERROR_CODES, DarajaErrorMessages
from .exceptions import (
    ClientError,
    IdempotencyError,
    InvalidCallbackUrlError,
    InvalidCheckoutRequestIdError,
    InvalidCredentialsError,
    InvalidPaymentAmountError,
    InvalidPhoneNumberError,
)

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        self._access_token = self._get_access_token()
        response = func(*args, **kwargs)
        return response

    return wrapper


def exponential_backoff_with_jitter(base_delay=1, max_delay=64, factor=2, jitter=0.1):
    """Exponential backoff retry policy."""
    delay = base_delay
    while True:
        yield delay + random.uniform(-jitter * delay, jitter * delay)
        delay = min(delay * factor, max_delay)


def retry_policy(retries=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                response = func(*args, **kwargs)
                if (
                    response.status_code in [500, 502, 503, 504]
                    and response.json().get("errorCode") not in IDEMPOTENCY_ERROR_CODES
                ):
                    backoff = exponential_backoff_with_jitter()
                    delay = next(backoff)
                    LOGGER.info("Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    return response

        return wrapper

    return decorator


def _handle_common_response_errors(response: Response):
    """Handle response after Daraja api post request."""
    data = response.json()

    # handle payload errors when sending post requests.
    if (
        response.status_code == 400
        and data.get("errorMessage") == DarajaErrorMessages.INVALID_AMOUNT.value
    ):
        msg = "Invalid payment amount."
        raise InvalidPaymentAmountError(msg)
    if (
        response.status_code == 400
        and data.get("errorMessage") == DarajaErrorMessages.INVALID_PHONE_NUMBER.value
    ):
        msg = "Invalid phone number."
        raise InvalidPhoneNumberError(msg)
    if (
        response.status_code == 400
        and data.get("errorMessage") == DarajaErrorMessages.INVALID_CALLBACK_URL.value
    ):
        msg = "Invalid callback url."
        raise InvalidCallbackUrlError(msg)

    # handle idempotency errors and any other error
    if 400 < response.status_code <= 500:
        LOGGER.debug(data, response.status_code)
        if (
            data.get("errorCode") in IDEMPOTENCY_ERROR_CODES
            and data.get("errorMessage")
            == DarajaErrorMessages.IDEMPOTENCY_ERROR_MSG.value
        ):
            msg = DarajaErrorMessages.IDEMPOTENCY_ERROR_MSG.value
            LOGGER.error(msg)
            raise IdempotencyError(msg)
        if (
            data.get("errorCode") in CLIENT_ERROR_CODES
            and data.get("errorMessage") == DarajaErrorMessages.WRONG_CREDENTIALS.value
        ):
            LOGGER.error(DarajaErrorMessages.WRONG_CREDENTIALS.value)
            raise InvalidCredentialsError("Invalid business shortcode or passkey.")
        if (
            data.get("errorCode") in CLIENT_ERROR_CODES
            and data.get("errorMessage")
            == DarajaErrorMessages.INVALID_CHECKOUT_REQUEST_ID.value
        ):
            msg = DarajaErrorMessages.INVALID_CHECKOUT_REQUEST_ID.value
            LOGGER.error(msg)
            raise InvalidCheckoutRequestIdError(msg)

        # catch unknown errors
        msg = f"{response.json()}, Status code: {response.status_code}"
        LOGGER.error(msg)
        raise Exception(msg)


def _handle_access_token_response_errors(instance, response):
    """Handle response errors after token request."""
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        instance._access_token_expiration_time = (
            int(response.json()["expires_in"]) + time.time()
        )
        return access_token
    elif response.status_code == 400:
        msg = "Failed to get access token. Invalid consumer key or consumer secret."  # noqa: E501
        LOGGER.error(msg)
        raise ClientError(msg)
    elif 400 <= response.status_code < 500:
        msg = "Invalid client credentials."
        raise ClientError(msg)
    else:
        # retry the current request if status code is above 500
        current_func = inspect.currentframe().f_code
        retry_policy()(current_func)


def _validate_phone_number(phone_number: str) -> None:
    """Validate phone number."""
    pattern = r"^(?:254|\+254|0)?((?:(?:7(?:(?:[01249][0-9])|(?:5[789])|(?:6[89])))|(?:1(?:[1][0-5])))[0-9]{6})$"  # noqa: E501

    if re.match(pattern, phone_number) is None:
        raise InvalidPhoneNumberError("Invalid phone number")


def _format_phone_number(phone_number: str) -> str:
    """Format phone number."""
    if phone_number.startswith("+"):
        return phone_number.strip("+")
    if phone_number.startswith("0"):
        return phone_number.replace("0", "254", 1)

    return phone_number


def _validate_amount(amount: int | float) -> None:
    """Validate payment amount."""
    if not isinstance(amount, (int, float)):
        raise InvalidPaymentAmountError("Provide a valid payment amount")

    if isinstance(amount, float) and not amount.is_integer():
        raise InvalidPaymentAmountError("Provide a valid payment amount")

    if amount <= 0:
        raise InvalidPaymentAmountError("Amount must be greater than 0")
