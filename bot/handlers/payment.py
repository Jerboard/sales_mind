from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice, SuccessfulPayment
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from datetime import datetime, timedelta

import re

import keyboards as kb
import utils as ut
import db
from settings import conf, log_error
from init import client_router, bot
from enums import CB, HandlerKey, Action


@client_router.callback_query(lambda cb: cb.data.startswith(CB.PAYMENT_START.value))
async def pay_start_cb(cb: CallbackQuery, state: FSMContext, session_id: str):
    await ut.send_payment_start(user_id=cb.from_user.id, msg_id=cb.message.message_id)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.PAY_START_CB.key,
        session=session_id
    )


@client_router.callback_query(lambda cb: cb.data.startswith(CB.PAYMENT_TARIFF.value))
async def payment_url(cb: CallbackQuery, state: FSMContext, session_id: str):
    _, tariff_id_str = cb.data.split(':')
    tariff_id = int(tariff_id_str)

    if tariff_id == 0:
        user = await db.User.get_by_id(cb.from_user.id)
        if user.is_used_trial:
            text = await db.Text.get_text(HandlerKey.PAYMENT_TRY_USED_TRIAL.key)
            await cb.answer(text, show_alert=True)

            # сохраняем действия пользователя
            await db.LogsUser.add(
                user_id=cb.from_user.id,
                action=HandlerKey.PAYMENT_TRY_USED_TRIAL.key,
                session=session_id
            )
            return

        await db.User.update(user_id=cb.from_user.id, is_used_trial=True)
        await ut.send_success_payment(
            user_id=cb.from_user.id,
        )

        # сохраняем действия пользователя
        await db.LogsUser.add(
            user_id=cb.from_user.id,
            action=HandlerKey.PAYMENT_USE_TRIAL.key,
            session=session_id
        )
        return

    tariff = await db.Tariff.get_by_id(tariff_id)
    text = await db.Text.get_text(HandlerKey.PAYMENT_URL.key)

    # await cb.message.edit_text(text, reply_markup=kb.get_back_kb(cb=CB.PAYMENT_START.value))

    await bot.send_invoice(
        chat_id=cb.from_user.id,
        title=tariff.name,
        description=text,
        payload=str(tariff.id),
        provider_token=conf.pay_token,
        currency='RUB',
        prices=[LabeledPrice(label=tariff.name, amount=tariff.price * 100)],
        need_phone_number=False
    )

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.PAYMENT_URL.key,
        comment=f'Тариф {tariff.name}',
        session=session_id
    )


# @client_router.pre_checkout_query_handler(lambda q: True)
@client_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    # Подтверждаем платеж
    await pre_checkout_q.answer(ok=True)


@client_router.message(lambda msg: msg.content_type == ContentType.SUCCESSFUL_PAYMENT.value)
async def process_successful_payment(msg: Message, session_id: str):
    tariff_id_str = msg.successful_payment.invoice_payload
    tariff_id = int(tariff_id_str)

    await ut.send_success_payment(
        user_id=msg.from_user.id,
        successful_payment=msg.successful_payment,
        tariff_id=tariff_id
    )

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=msg.from_user.id,
        action=HandlerKey.PAYMENT_SUCCESS.key,
        session=session_id
    )



