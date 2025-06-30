import aiohttp
from uuid import uuid4

import db
from settings import conf


async def create_lava_invoice(
        tariff: db.Tariff,
        # order_id: str,
        user_id: int
) -> dict:

    url = "https://api.lava.ru/business/invoice/create"
    headers = {
        "Authorization": f"Bearer {conf.pay_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": tariff.price,
        "order_id": uuid4(),
        "wallet_to": conf.wallet_id,
        "comment": tariff.description,
        'custom_fields': f'{user_id}:{tariff.id}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            # if resp.status == 200:
            data = await resp.json()
            return data

# Пример вызова:
# response = await create_lava_invoice(api_key="тут_твой_ключ", wallet_id="тут_id", amount=100, order_id="test1", comment="Оплата тест")




