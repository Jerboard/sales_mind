import os

from zoneinfo import ZoneInfo


class Config:
    debug = bool(int(os.getenv('DEBUG')))

    if debug:
        # token = os.getenv("TOKEN_TEST")
        token = os.getenv("TOKEN")
        shop_id = os.getenv("YK_SHOP_ID_TEST")
        pay_secret = os.getenv("YK_SECRET_TEST")
        pay_token = os.getenv("YK_PAY_TOKEN_TEST")
    else:
        token = os.getenv("TOKEN")
        shop_id = os.getenv("YK_SHOP_ID_TEST")
        pay_secret = os.getenv("YK_SECRET_TEST")
        pay_token = os.getenv("YK_PAY_TOKEN_TEST")

    gpt_token = os.getenv('GPT_TOKEN')

    # pay_key = os.getenv("PAY_KEY_TEST")
    # wallet_id = os.getenv("WALLET_ID_TEST")
    # secret_1 = os.getenv('SECRET_1')
    # secret_2 = os.getenv('SECRET_2')

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
