# pydaraja

## Description
This is a python wrapper that handles payment requests through the Daraja Mpesa API.

Daraja API services offered by pydaraja are:
- Lipa na M-PESA online API also known as M-PESA express (STK Push/NI push)
- STK push query API -> Used to check the status of Lipa na Mpesa online payment

More services will come soon.

## Installation
```
pip install -U pydaraja
```

## Usage
```
from pydaraja import payment

payment.CONSUMER_KEY = "YOUR_CONSUMER_KEY"
payment.CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
payment.BUSINESS_SHORTCODE = "YOUR_BUSINESS_SHORTCODE"
payment.PASSKEY = "YOUR_PASSKEY"
payment.CALLBACK_URL = "YOUR_CALLBACK_URL"

payment.ACCOUNT_REFERENCE = "YOUR_ACCOUNT_REFERENCE"
payment.TRANSACTION_DESC = "YOUR_TRANSACTION_DESCRIPTION"

response = payment.trigger_stk_push(phone_number="+254700000000", amount=1)
print(response.json())

# use checkout_request_id from the above stk push as parameter for the function below
stk_query = payment.query_stk_push(your_checkout_request_id)
print(stk_query.json())

```

## Contribute

Read the [CONTRIBUTING.md](https://github.com/raykipkorir/pydaraja/blob/main/CONTRIBUTING.md) file.
