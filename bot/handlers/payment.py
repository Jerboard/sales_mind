from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice, SuccessfulPayment
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.message_entity_type import MessageEntityType
from datetime import datetime, timedelta

import json

import keyboards as kb
import utils as ut
import db
from settings import conf, log_error
from init import client_router, bot
from enums import CB, HandlerKey, PayType


@client_router.callback_query(lambda cb: cb.data.startswith(CB.PAYMENT_START.value))
async def pay_start_cb(cb: CallbackQuery, state: FSMContext, session_id: str, user: db.User):
    await ut.send_payment_start(user_id=cb.from_user.id, msg_id=cb.message.message_id, user=user)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.PAY_START_CB.key,
        session=session_id
    )


@client_router.callback_query(lambda cb: cb.data.startswith(CB.PAYMENT_TARIFF.value))
async def payment_url(cb: CallbackQuery, state: FSMContext, session_id: str, user: db.User):
    _, pay_type, tariff_id_str = cb.data.split(':')
    tariff_id = int(tariff_id_str)

    if pay_type == PayType.TARIFF.value and tariff_id == 0:
        if user.is_used_trial:
            text = await db.Text.get_text(HandlerKey.PAYMENT_TRY_USED_TRIAL.key)
            await cb.answer(text, show_alert=True)

            action = HandlerKey.PAYMENT_TRY_USED_TRIAL.key

        else:
            await db.User.update(user_id=user.id, is_used_trial=True)
            await ut.send_success_payment(
                user_id=user.id,
            )
            action = HandlerKey.PAYMENT_USE_TRIAL.key

    elif not user.email:
        text = await db.Text.get_text(HandlerKey.PAYMENT_URL_EMAIL.key)
        await state.set_state(HandlerKey.PAYMENT_URL_EMAIL.key)
        await state.update_data(data={'pay_type': pay_type, 'tariff_id': tariff_id})
        await cb.message.answer(text=text, reply_markup=kb.get_back_kb())

        action = HandlerKey.PAYMENT_URL_EMAIL.key

    else:
        await ut.create_pay_link(
            user=user, tariff_id=tariff_id, pay_type=pay_type, msg_id=cb.message.message_id, session_id=session_id
        )
        return

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=user.id,
        action=action,
        session=session_id
    )


@client_router.callback_query(lambda cb: cb.data.startswith(CB.PAYMENT_REQUESTS.value))
async def payment_requests(cb: CallbackQuery, state: FSMContext, session_id: str, user: db.User):
    requests = await db.Request.get_all()
    text = await db.Text.get_text(HandlerKey.PAYMENT_URL_REQUEST_VIEW.key)

    await cb.message.edit_text(text=text, reply_markup=kb.get_requests_kb(requests))

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=user.id,
        action=HandlerKey.PAYMENT_URL_REQUEST_VIEW.key,
        session=session_id
    )


@client_router.message(StateFilter(HandlerKey.PAYMENT_URL_EMAIL.key))
async def payment_url_email(msg: Message, state: FSMContext, session_id: str, user: db.User):
    if msg.entities and msg.entities[0].type == MessageEntityType.EMAIL.value:
        await db.User.update(user_id=msg.from_user.id, email=msg.text)
        data = await state.get_data()
        await state.clear()
        await ut.create_pay_link(
            user=user,
            tariff_id=data.get('tariff_id'),
            pay_type=data.get('pay_type'),
            session_id=session_id
        )
    
    else:
        text = await db.Text.get_text(HandlerKey.PAYMENT_ADD_EMAIL_ERROR.key)
        await msg.answer(text, reply_markup=kb.get_back_kb(cb=CB.PAYMENT_START.value))

        # сохраняем действия пользователя
        await db.LogsUser.add(
            user_id=msg.from_user.id,
            action=HandlerKey.PAYMENT_ADD_EMAIL_ERROR.key,
            session=session_id
        )
        return
    