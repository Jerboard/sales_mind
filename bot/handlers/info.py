from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import keyboards as kb
import utils as ut
import db
from settings import conf, log_error
from init import client_router, bot
from enums import CB, MenuCommand, Action


@client_router.callback_query(lambda cb: cb.data.startswith(CB.INFO_START.value))
async def info(cb: CallbackQuery, state: FSMContext):
    await ut.send_info_start(user_id=cb.from_user.id, msg_id=cb.message.message_id)

    # text = 'Инфо о проекте'
    # info = await db.Info.get_all()
    # await cb.message.edit_text(text, reply_markup=kb.get_info_menu_kb(info))


@client_router.callback_query(lambda cb: cb.data.startswith(CB.INFO_TEXT.value))
async def payment_start(cb: CallbackQuery, state: FSMContext):
    _, info_id_str, back = cb.data.split(':')
    info_id = int(info_id_str)

    info = await db.Info.get_by_id(info_id)
    await cb.message.edit_text(
        info.description,
        reply_markup=kb.get_back_kb(cb=back)
    )