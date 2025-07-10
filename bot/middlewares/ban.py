from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

import db
import keyboards as kb


# проверяет блокированных пользователей
class BanCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        # Проверяем, что событие - это сообщение
        user_id = None
        cb = 'fff'
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            cb = event.data.split(':')[0]

        if user_id:
            user = await db.User.get_by_id(user_id)
            if user and user.is_ban:
                text = f'❌ Вам закрыт доступ'
                if isinstance(event, Message):
                    await event.answer(text)
                else:
                    await event.message.answer(text)

                return

            state: FSMContext = data.get("state")
            current_state = await state.get_state()
            # print(f'current_state: {current_state}')
            # if (cb.startswith('gpt_') or current_state) and (user.requests_remaining == 0 or user.subscription_end < datetime.now()):
            if (cb.startswith('gpt_') or current_state) and user.requests_remaining == 0:
                text = f'❌ Увас не осталось запросов'
                markup = kb.get_start_payment_kb()

                if isinstance(event, Message):
                    await event.answer(text, reply_markup=markup)
                else:
                    await event.message.answer(text, reply_markup=markup)

                return


        return await handler(event, data)


