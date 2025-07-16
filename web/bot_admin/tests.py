import requests


def test_payments():
    url = "http://localhost:8000/api/payment"
    payload = {
        "type": "notification",
        "event": "payment.succeeded",
        "object": {
            "id": "3008058f-000f-5000-b000-14e427e062a6",
            "status": "succeeded",
            "amount": {
                "value": "10.00",
                "currency": "RUB"
            },
            "income_amount": {
                "value": "9.65",
                "currency": "RUB"
            },
            "description": "Подключение пробного периода",
            "recipient": {
                "account_id": "1123576",
                "gateway_id": "2495541"
            },
            "payment_method": {
                "type": "bank_card",
                "id": "3008058f-000f-5000-b000-14e427e062a6",
                "saved": False,
                "status": "inactive",
                "title": "Bank card *4444",
                "card": {
                    "first6": "555555",
                    "last4": "4444",
                    "expiry_year": "2025",
                    "expiry_month": "12",
                    "card_type": "MasterCard",
                    "card_product": {
                        "code": "E"
                    },
                    "issuer_country": "US"
                }
            },
            "captured_at": "2025-07-15T06:16:09.873Z",
            "created_at": "2025-07-15T06:14:39.516Z",
            "test": True,
            "refunded_amount": {
                "value": "0.00",
                "currency": "RUB"
            },
            "paid": True,
            "refundable": True,
            "metadata": {
                "user_id": "524275902",
                "cms_name": "yookassa_sdk_python",
                "tariff_id": "1",
                "pay_type": "tariff",
                # "pay_type": "request",
                "session_id": "ddddddddddddd",
            },
            "authorization_details": {
                "rrn": "810626339992811",
                "auth_code": "495813",
                "three_d_secure": {
                    "applied": False,
                    "method_completed": False,
                    "challenge_completed": False
                }
            }
        }
    }

    response = requests.post(url, json=payload)
    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.text}")


if __name__ == '__main__':
    test_payments()
