# pydaraja
[![PyPI version](https://badge.fury.io/py/pydaraja.svg)](https://badge.fury.io/py/pydaraja)
[![Wheel Status](https://img.shields.io/badge/wheel-yes-green.svg)](https://pypi.python.org/pypi/pydaraja/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
## Description
This Python wrapper allows developers to seamlessly interact with the MPESA's Daraja API and manage payment requests within their Python applications.

 It streamlines and abstracts the complexity of integrating with the MPESA's Daraja API, providing developers with a convenient and efficient means of handling payment transactions

Daraja API services offered by pydaraja are:
- Lipa na M-PESA online API also known as M-PESA express (STK Push/NI push)
- STK push query API -> Used to check the status of Lipa na Mpesa online payment

More services will come soon.

## Installation
```
pip install -U pydaraja
```

## Usage
1. Lipa na Mpesa Online API (STK push) and STK push query API.


```python
from pydaraja import MpesaPaymentGateway

# Create MpesaPaymentGateway instance
mpesa = MpesaPaymentGateway(
    consumer_key="consumer_key",
    consumer_secret="consumer_secret",
    business_shortcode="business_shortcode",
    passkey="passkey"
    endpoint="https://sandbox.safaricom.co.ke",
)

# Trigger STK push prompt
response = mpesa.trigger_stk_push(phone_number="+254700000000", amount=1, callback_url="https://example.com")

print(response.json())
# Output
{
    'MerchantRequestID': '2654-4b64-97ff-b827b542881d164797',
    'CheckoutRequestID': 'ws_CO_18072024175449513769356298',
    'ResponseCode': '0',
    'ResponseDescription': 'Success. Request accepted for processing',
    'CustomerMessage': 'Success. Request accepted for processing'
}


# use checkout_request_id from the above stk push as parameter for the function below
response = mpesa.query_stk_push(checkout_request_id=your_checkout_request_id)

print(response.json())
# Output
{
    'ResponseCode': '0',
    'ResponseDescription': 'The service request has been accepted successsfully',
    'MerchantRequestID': '2654-4b64-97ff-b827b542881d164797',
    'CheckoutRequestID': 'ws_CO_18072024175449513769356298',
    'ResultCode': '0',
    'ResultDesc': 'The service request is processed successfully.'
 }
```

## Contributing
To contribute to this project, we kindly request you to review the [CONTRIBUTING.md](https://github.com/raykipkorir/pydaraja/blob/main/CONTRIBUTING.md)  file for detailed guidelines.


## License
This python package is available as open source under the terms of the [MIT License](https://opensource.org/license/mit/)
