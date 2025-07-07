from aiogram import Dispatcher, Router
from aiogram.types.bot_command import BotCommand
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import redis.asyncio as redis
import asyncio
import uvloop

from sqlalchemy.ext.asyncio import create_async_engine
from openai import AsyncOpenAI

from settings import conf
from enums.base import MenuCommand


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()
bot = Bot(
    token=conf.token,
    loop=loop,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


client_openai = AsyncOpenAI()

client_redis = redis.Redis(host=conf.redis_host, port=conf.redis_port, db=0, decode_responses=True)

main_router = Router()
client_router = Router()
error_router = Router()


ENGINE = create_async_engine(url=conf.db_url)


async def set_main_menu():
    await bot.set_my_commands([
        BotCommand(command=cmd.command, description=cmd.label)
        for cmd in MenuCommand
    ])
