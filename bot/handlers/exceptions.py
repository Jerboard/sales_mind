from aiogram.types import ErrorEvent, Message, CallbackQuery

from init import error_router
from settings import log_error, conf
import utils as ut
import db

from enums import HandlerKey


if not conf.debug:
    @error_router.errors()
    async def error_handler(ex: ErrorEvent, session_id: str):
        tb, msg = log_error (ex)
        user_id = ex.update.message.from_user.id if ex.update.message else None

        await db.LogsError.add(user_id=user_id, traceback=tb, message=msg)

        if user_id:
            await db.LogsUser.add(
                user_id=user_id,
                action=HandlerKey.ERROR.key,
                session=session_id
            )


@error_router.message()
async def free_msg_hnd(msg: Message, user: db.User, session_id: str):
    print(f'free_msg_hnd:\n{msg.content_type}\n{msg.text}')
    text = await db.Text.get_text(HandlerKey.EMPTY_REQUEST.key)

    await msg.answer(text)
    await ut.send_gpt_start(user=user)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=msg.from_user.id,
        action=HandlerKey.EMPTY_REQUEST.key,
        session=session_id
    )


# проверяет подписку, в случае удачи пропускает
@error_router.callback_query()
async def free_cb_hnd(cb: CallbackQuery):
    print(f'free_cb_hnd:\n{cb.data}')

    await cb.answer('🛠 Функция в разработке', show_alert=True)
