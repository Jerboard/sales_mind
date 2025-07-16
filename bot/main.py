import asyncio
import logging
import sys

from aiogram import Dispatcher
from datetime import datetime

import db
from init import set_main_menu, bot
from settings import conf, log_error
from db.base import init_models
from handlers.main_menu import main_router
from handlers.exceptions import error_router
from handlers import client_router
from middlewares import OneBigBeautifulMiddleware


dp = Dispatcher()
dp.message.middleware(OneBigBeautifulMiddleware())
dp.callback_query.middleware(OneBigBeautifulMiddleware())
dp.errors.middleware(OneBigBeautifulMiddleware())


async def main() -> None:
    await db.Text.add_new_texts_on_start()
    await set_main_menu()

    dp.include_router(main_router)
    dp.include_router(client_router)
    dp.include_router(error_router)
    await dp.start_polling(bot)
    await bot.session.close()


if __name__ == "__main__":
    if conf.debug:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start bot', wt=False)
    asyncio.run(main())
