from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

import db


class BanCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        # Проверяем, что событие - это сообщение
        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

        if user_id:
            user = await db.User.get_by_id(user_id)
            if user.is_ban:
                text = f'❌ Вам закрыт доступ'
                if isinstance(event, Message):
                    await event.answer(text)
                else:
                    await event.message.answer(text)

                return

        return await handler(event, data)


