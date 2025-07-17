from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime, timezone

import db
import keyboards as kb
import utils as ut
from enums import HandlerKey, CB


# проверяет блокированных пользователей
class OneBigBeautifulMiddleware(BaseMiddleware):
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
            user = await db.User.get_full_user(user_id)
            session_id = await ut.get_or_create_session(event.from_user.id)

            data['session_id'] = session_id
            data['user'] = user

            if user and user.is_ban:
                text = await db.Text.get_text(HandlerKey.BAN.key)

                if isinstance(event, Message):
                    await event.answer(text)
                else:
                    await event.message.answer(text)

                # сохраняем действия пользователя
                await db.LogsUser.add(
                    user_id=user_id,
                    action=HandlerKey.PAYMENT_DISALLOW.key,
                    session=session_id
                )

                return

            state: FSMContext = data.get("state")
            current_state = await state.get_state()
            is_unlimited_tariff = user.tariff.is_unlimited if user.tariff else False
            requests_remaining = user.requests_remaining if not is_unlimited_tariff else 1
            if (
                    (cb.startswith('gpt_') or current_state == CB.GPT_PROMPT.value)
                    and
                    (requests_remaining == 0 or user.subscription_end < datetime.now(timezone.utc))
            ):
                text = await db.Text.get_text(HandlerKey.PAYMENT_DISALLOW.key)
                markup = kb.get_start_payment_kb()

                if isinstance(event, Message):
                    await event.answer(text, reply_markup=markup)
                else:
                    await event.message.answer(text, reply_markup=markup)

                # сохраняем действия пользователя
                await db.LogsUser.add(
                    user_id=user_id,
                    action=HandlerKey.PAYMENT_DISALLOW.key,
                    session=session_id
                )

                return

        return await handler(event, data)
