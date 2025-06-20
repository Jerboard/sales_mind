import os

from zoneinfo import ZoneInfo


class Config:
    debug = bool(int(os.getenv('DEBUG')))

    if debug:
        token = os.getenv("TOKEN_TEST")
        pay_key = os.getenv("PAY_KEY_TEST")
        wallet_id = os.getenv("WALLET_ID_TEST")
    else:
        token = os.getenv("TOKEN")
        pay_key = os.getenv("PAY_KEY_TEST")
        wallet_id = os.getenv("WALLET_ID_TEST")

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

    gpt_token = os.getenv('GPT_TOKEN')


conf = Config()
