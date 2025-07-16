import os

from zoneinfo import ZoneInfo


class Config:
    debug = bool(int(os.getenv('DEBUG')))

    if debug:
        token = os.getenv("TOKEN_TEST")
        shop_id = os.getenv("YOOKASSA_SHOP_ID_TEST")
        pay_key = os.getenv("YOOKASSA_SECRET_KEY_TEST")

        # shop_id = os.getenv("YOOKASSA_SHOP_ID")
        # pay_key = os.getenv("YOOKASSA_SECRET_KEY")

        pay_token = os.getenv("YK_PAY_TOKEN")
        notice_url = 'https://webhook.site/543933ee-1b55-4b79-97a1-46fd404395df'

        bot_username = 'tushchkan_test_1_bot'
    else:
        token = os.getenv("TOKEN")
        shop_id = os.getenv("YOOKASSA_SHOP_ID")
        pay_key = os.getenv("YOOKASSA_SECRET_KEY")
        pay_token = os.getenv("YK_PAY_TOKEN")

        notice_url = 'http://91.218.143.134/api/payment'

        bot_username = 'SalesMindAI_bot'

    gpt_token = os.getenv('GPT_TOKEN')
    pay_return_url = f'https://t.me/{bot_username}'

    celery_project = os.getenv('COMPOSE_PROJECT_NAME')

    # Redis connection settings REDIS_HOST
    redis_host = os.getenv("REDIS_HOST")
    redis_port = int(os.getenv("REDIS_PORT"))
    session_ttl = 3600  # 1 hour in seconds

    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('POSTGRES_DB')
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_url = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    tz = ZoneInfo('Europe/Moscow')

    date_format = '%d.%m.%Y'
    time_format = '%H:%M'
    datetime_format = '%H:%M %d.%m.%Y'


conf = Config()
