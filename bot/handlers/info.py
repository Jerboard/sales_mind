from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import keyboards as kb
import utils as ut
import db
from settings import conf, log_error
from init import client_router, bot
from enums import CB, HandlerKey, Action


@client_router.callback_query(lambda cb: cb.data.startswith(CB.HELP_START.value))
async def help_start_cb(cb: CallbackQuery, state: FSMContext, session_id: str):
    await ut.send_info_start(user_id=cb.from_user.id, msg_id=cb.message.message_id)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.HELP_START_CB.key,
        session=session_id
    )


@client_router.callback_query(lambda cb: cb.data.startswith(CB.HELP_TEXT.value))
async def help_text(cb: CallbackQuery, state: FSMContext, session_id: str):
    _, info_id_str, back = cb.data.split(':')
    info_id = int(info_id_str)

    info = await db.Info.get_by_id(info_id)
    await cb.message.edit_text(
        info.description,
        reply_markup=kb.get_back_kb(cb=back)
    )

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.HELP_TEXT.key,
        comment=info.name,
        session=session_id
    )
