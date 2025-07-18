import requests


def test_payments():
    url = "http://localhost:8000/api/payment"
    # url = "https://salesmindpayments.ru/api/payment"
    payload = {
      "type" : "notification",
      "event" : "payment.succeeded",
      "object" : {
        "id" : "300ac6b1-000f-5001-8000-15239bf518f6",
        "status" : "succeeded",
        "amount" : {
          "value" : "499.00",
          "currency" : "RUB"
        },
        "income_amount" : {
          "value" : "477.54",
          "currency" : "RUB"
        },
        "description" : "🟢 Lite — 499 ₽ / мес",
        "recipient" : {
          "account_id" : "1120916",
          "gateway_id" : "2485604"
        },
        "payment_method" : {
          "type" : "sberbank",
          "id" : "300ac6b1-000f-5001-8000-15239bf518f6",
          "saved" : False,
          "status" : "inactive",
          "card" : {
            "first6" : "533669",
            "last4" : "3348",
            "expiry_year" : "2026",
            "expiry_month" : "05",
            "card_type" : "MasterCard"
          }
        },
        "captured_at" : "2025-07-17T08:24:15.465Z",
        "created_at" : "2025-07-17T08:23:13.703Z",
        "test" : False,
        "refunded_amount" : {
          "value" : "0.00",
          "currency" : "RUB"
        },
        "paid" : True,
        "refundable" : True,
        "receipt_registration" : "pending",
        "metadata" : {
          "session_id" : "4605cfc0-d687-44be-8f09-2b7f8bb86a36",
          "pay_type" : "tariff",
          # "pay_type" : "request",
          "tariff_id" : "3",
          "user_id" : "524275902",
          "cms_name" : "yookassa_sdk_python"
        },
        "authorization_details" : {
          "rrn" : "519863843398",
          "auth_code" : "210256",
          "three_d_secure" : {
            "applied" : False
      }
    }
  }
}
    # payload = {
    #     "type": "notification",
    #     "event": "payment.succeeded",
    #     "object": {
    #         "id": "3008058f-000f-5000-b000-14e427e062a6",
    #         "status": "succeeded",
    #         "amount": {
    #             "value": "10.00",
    #             "currency": "RUB"
    #         },
    #         "income_amount": {
    #             "value": "9.65",
    #             "currency": "RUB"
    #         },
    #         "description": "Подключение пробного периода",
    #         "recipient": {
    #             "account_id": "1123576",
    #             "gateway_id": "2495541"
    #         },
    #         "payment_method": {
    #             "type": "bank_card",
    #             "id": "3008058f-000f-5000-b000-14e427e062a6",
    #             "saved": False,
    #             "status": "inactive",
    #             "title": "Bank card *4444",
    #             "card": {
    #                 "first6": "555555",
    #                 "last4": "4444",
    #                 "expiry_year": "2025",
    #                 "expiry_month": "12",
    #                 "card_type": "MasterCard",
    #                 "card_product": {
    #                     "code": "E"
    #                 },
    #                 "issuer_country": "US"
    #             }
    #         },
    #         "captured_at": "2025-07-15T06:16:09.873Z",
    #         "created_at": "2025-07-15T06:14:39.516Z",
    #         "test": True,
    #         "refunded_amount": {
    #             "value": "0.00",
    #             "currency": "RUB"
    #         },
    #         "paid": True,
    #         "refundable": True,
    #         "metadata": {
    #             "user_id": "524275902",
    #             "cms_name": "yookassa_sdk_python",
    #             "tariff_id": "1",
    #             "pay_type": "tariff",
    #             # "pay_type": "request",
    #             "session_id": "ddddddddddddd",
    #         },
    #         "authorization_details": {
    #             "rrn": "810626339992811",
    #             "auth_code": "495813",
    #             "three_d_secure": {
    #                 "applied": False,
    #                 "method_completed": False,
    #                 "challenge_completed": False
    #             }
    #         }
    #     }
    # }

    response = requests.post(url, json=payload)
    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.text}")


if __name__ == '__main__':
    test_payments()
