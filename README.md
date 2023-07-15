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
- Transaction status API -> Check the status of a transaction

- Account balance API -> The Account Balance API is used to request the account balance of a short code. This can be used for both B2C, buy goods and pay bill accounts.

More services will come soon.

## Installation
```
pip install -U pydaraja
```

## Usage
1. Lipa na Mpesa Online API (STK push) and STK push query API.


```
from pydaraja import config, payment


# setup configurations
config.CONSUMER_KEY = "YOUR_CONSUMER_KEY"
config.CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
config.BUSINESS_SHORTCODE = "YOUR_BUSINESS_SHORTCODE"
config.PASSKEY = "YOUR_PASSKEY"
config.CALLBACK_URL = "YOUR_CALLBACK_URL"

# optional
config.ACCOUNT_REFERENCE = "YOUR_ACCOUNT_REFERENCE" # default is "Pydaraja"
config.TRANSACTION_DESC = "YOUR_TRANSACTION_DESCRIPTION" # default is "Python wrapper for mpesa api"


response = payment.trigger_stk_push(phone_number="+254700000000", amount=1)
print(response.json())

# use checkout_request_id from the above stk push as parameter for the function below
stk_query = payment.query_stk_push(your_checkout_request_id)
print(stk_query.json())

```
2. Transaction status API and Account Balance API
```
from pydaraja import config, payment


# setup configurations
config.CONSUMER_KEY = "YOUR_CONSUMER_KEY"
config.CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
config.SECURITY_CREDENTIAL = "YOUR SECURITY_CREDENTIAL"
config.PARTY_A = "YOUR_BUSINESS_SHORTCODE"
config.IDENTIFIER_TYPE = "YOUR_IDENTIFIER_TYPE"
config.RESULT_URL = "YOUR_RESULT_URL"
config.QUEUE_TIMEOUT_URL = "YOUR_QUEUE_TIMEOUT_URL"

# optional
config.INITIATOR = "INITIATOR" # default is "testapiuser"
config.REMARKS = "YOUR_REMARKS" # default is "OK"
config.OCCASSION = "YOUR_OCCASSION" # default is "OK"

# transaction status
response = payment.transaction_status(<your_transaction_id>)
print(response.json())

# account balance
response = payment.account_balance()
print(response.json())

```

## Contributing
To contribute to this project, we kindly request you to review the [CONTRIBUTING.md](https://github.com/raykipkorir/pydaraja/blob/main/CONTRIBUTING.md)  file for detailed guidelines.


## License
This python package is available as open source under the terms of the [MIT License](https://opensource.org/license/mit/)
