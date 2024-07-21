"""Custom exceptions."""


class ClientError(Exception):
    pass


class IdempotencyError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidUrlError(Exception):
    pass


class InvalidPaymentAmountError(Exception):
    pass


class InvalidPhoneNumberError(Exception):
    pass


class InvalidCallbackUrlError(Exception):
    pass


class InvalidCheckoutRequestIdError(Exception):
    pass
