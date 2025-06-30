from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.parse_mode import ParseMode

import re

import keyboards as kb
import utils as ut
import db
from settings import conf, log_error
from init import client_router, bot
from enums import CB, HandlerKey, Action


@client_router.callback_query(lambda cb: cb.data.startswith(CB.PAYMENT_START.value))
async def pay_start_cb(cb: CallbackQuery, state: FSMContext):
    await ut.send_payment_start(user_id=cb.from_user.id, msg_id=cb.message.message_id)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.PAY_START_CB.key,
    )


@client_router.callback_query(lambda cb: cb.data.startswith(CB.PAYMENT_TARIFF.value))
async def payment_url(cb: CallbackQuery, state: FSMContext):
    _, tariff_id_str = cb.data.split(':')
    tariff_id = int(tariff_id_str)

    tariff = await db.Tariff.get_by_id(tariff_id)

    # url = await ut.create_lava_invoice(tariff=tariff, user_id=cb.from_user.id)
    text = await db.Text.get_text(HandlerKey.PAYMENT_URL.key)

    # text = (
    #     '<b>Формируем ссылку, отправляем на оплату</b>'
    # )
    await cb.message.edit_text(text, reply_markup=kb.get_back_kb(cb=CB.PAYMENT_START.value))

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.PAYMENT_URL.key,
        comment=f'Тариф {tariff.name}'
    )




