from aiogram.types import ErrorEvent, Message, CallbackQuery

from init import error_router
from settings import log_error, conf
import utils as ut
from db import LogsError


if not conf.debug:
    @error_router.errors()
    async def error_handler(ex: ErrorEvent):
        tb, msg = log_error (ex)
        user_id = ex.update.message.from_user.id if ex.update.message else None

        await LogsError.add(user_id=user_id, traceback=tb, message=msg)


@error_router.message()
async def free_msg_hnd(msg: Message):
    print(f'free_msg_hnd:\n{msg.content_type}\n{msg.text}')

    await msg.answer('🤷‍♂️ Не понял твоего вопроса, выбери сначала контекст')
    await ut.send_gpt_start(user_id=msg.from_user.id)



# проверяет подписку, в случае удачи пропускает
@error_router.callback_query()
async def free_cb_hnd(cb: CallbackQuery):
    print(f'free_cb_hnd:\n{cb.data}')

    await cb.answer('🛠 Функция в разработке', show_alert=True)
