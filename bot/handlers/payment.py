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
from enums import CB, MenuCommand, Action


@client_router.callback_query(lambda cb: cb.data.startswith(CB.PAYMENT_START.value))
async def payment_start(cb: CallbackQuery, state: FSMContext):
    await ut.send_payment_start(user_id=cb.from_user.id, msg_id=cb.message.message_id)
    # tariffs = await db.Tariff.get_all()
    #
    # text = ''
    # for tariff in tariffs:
    #     text += f'{tariff.description}\n\n'
    #
    # text += f'<b>🎁 Попробовать бесплатно — 5 генераций для знакомства</b>'
    #
    # await cb.message.edit_text(text, reply_markup=kb.get_payment_kb(tariffs))


@client_router.callback_query(lambda cb: cb.data.startswith(CB.PAYMENT_TARIFF.value))
async def payment_start(cb: CallbackQuery, state: FSMContext):
    _, tariff_id_str = cb.data.split(':')
    text = (
        '<b>Формируем ссылку, отправляем на оплату</b>'
    )
    await cb.message.edit_text(text, reply_markup=kb.get_back_kb(cb=CB.PAYMENT_START.value))




