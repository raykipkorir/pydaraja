"""Mpesa gateway tests."""

from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest
from requests import ConnectionError, Session
from requests.models import Response

from pydaraja import MpesaPaymentGateway
from pydaraja.exceptions import InvalidUrlError


class TestMpesaGateway(TestCase):
    """Mpesa payment gateway tests."""

    @patch.object(Session, "request", autospec=True)
    def setUp(self, mock_session) -> None:
        """SetUp."""
        data = {"access_token": "sdjklsndflkj2398", "expires_in": "3600"}
        response = Response()
        response.status_code = 200
        response._content = "".encode("utf-8")
        response.json = MagicMock(return_value=data)
        mock_session.return_value = response

        self.mpesa = MpesaPaymentGateway(
            consumer_key="RANDOMKEY240",
            consumer_secret="RANDOMSECRET2023048",
            business_shortcode="28930",
            endpoint="https://daraja.com",
            passkey="aksfjkew9238923nma",
        )

    @patch.object(Session, "request", autospec=True)
    def test_trigger_stk_push(self, mock_session):
        """Test trigger stk push prompt."""
        data = {
            "MerchantRequestID": "6e86-45dd-91ac-fd5d4178ab523860487",
            "CheckoutRequestID": "ws_CO_25072024165320435769356298",
            "ResponseCode": "0",
            "ResponseDescription": "Success. Request accepted for processing",
            "CustomerMessage": "Success. Request accepted for processing",
        }
        response = Response()
        response.status_code = 200
        response._content = "".encode("utf-8")
        response.json = MagicMock(return_value=data)
        mock_session.return_value = response

        response2 = self.mpesa.trigger_stk_push(
            phone_number="0700000000", amount=1, callback_url="https://example.com"
        )

        assert response2.status_code == 200

    @patch.object(Session, "request", autospec=True)
    def test_query_stk_push(self, mock_session):
        """Test query stk push prompt."""
        data = {
            "ResponseCode": "0",
            "ResponseDescription": "The service request has been accepted successsfully",
            "MerchantRequestID": "2654-4b64-97ff-b827b542881d164797",
            "CheckoutRequestID": "ws_CO_18072024175449513769356298",
            "ResultCode": "0",
            "ResultDesc": "The service request is processed successfully.",
        }
        response = Response()
        response.status_code = 200
        response._content = "".encode("utf-8")
        response.json = MagicMock(return_value=data)
        mock_session.return_value = response

        response = self.mpesa.query_stk_push(checkout_request_id="WSjlvir309")

        assert response.status_code == 200

    @patch.object(Session, "request", autospec=True)
    def test_invalid_url_error_is_raised(self, mock_session):
        """Test trigger stk push prompt."""
        mock_session.side_effect = ConnectionError("Error.")
        with pytest.raises(InvalidUrlError):
            self.mpesa2 = MpesaPaymentGateway(
                consumer_key="RANDOMKEY240",
                consumer_secret="RANDOMSECRET2023048",
                business_shortcode="28930",
                endpoint="https:daraja.com",
                passkey="aksfjkew9238923nma",
            )
