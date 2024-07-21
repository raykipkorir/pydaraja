"""Constants."""

from enum import Enum

IDEMPOTENCY_ERROR_CODES = ("500.001.1001", "500.003.02")
CLIENT_ERROR_CODES = ("500.001.1001",)


class DarajaErrorMessages(Enum):
    """Daraja Error Messages."""

    INVALID_PHONE_NUMBER = "Bad Request - Invalid PhoneNumber"
    INVALID_AMOUNT = "Bad Request - Invalid Amount"
    INVALID_CALLBACK_URL = "Bad Request - Invalid CallBackURL"
    INVALID_CHECKOUT_REQUEST_ID = "This transaction does not exist"
    IDEMPOTENCY_ERROR_MSG = "Unable to lock subscriber, a transaction is already in process for the current subscriber"
    WRONG_CREDENTIALS = "Wrong credentials"
