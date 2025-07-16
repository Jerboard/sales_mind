from yookassa import Payment
from yookassa import Configuration
from yookassa.payment import PaymentResponse
from yookassa.domain.notification import WebhookNotification
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import logging

from settings import conf

logger = logging.getLogger(__name__)

Configuration.account_id = conf.shop_id
Configuration.secret_key = conf.pay_key


# "Для управления оплатой"
def get_pay_link(
        user_id: int,
        tariff_id: int,
        email: str,
        description: str,
        amount: int,
        pay_type: str,
        session_id: str,
) -> PaymentResponse:
    return Payment.create(params={
        "amount": {
            "value": str(amount),
            "currency": 'RUB'
        },
        "confirmation": {
            "type": "redirect",
            "return_url": conf.pay_return_url,
        },
        "capture": True,
        "description": description,
        "metadata": {
            "user_id": user_id,
            "tariff_id": tariff_id,
            "pay_type": pay_type,
            "session_id": session_id,
        },
        "receipt": {
            "customer": {
                "email": email
            },
            "items": [
                {
                    "description": description,
                    "quantity": "1.00",
                    "amount": {
                        "value": amount,
                        "currency": "RUB"
                    },
                    "vat_code": "1",
                    "payment_mode": "full_payment",
                    "payment_subject": "service"
                }
            ]
        },
    },
        idempotency_key=uuid4()
    )
