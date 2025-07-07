from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

import utils as ut


# создаёт сессии
class SessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        if event.from_user and event.from_user.id:
            session_id = await ut.get_or_create_session(event.from_user.id)
            data['session_id'] = session_id

        return await handler(event, data)
