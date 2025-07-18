from aiogram.types import SuccessfulPayment, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

import db
from init import bot
import keyboards as kb
from settings import conf, log_error
from utils.gpt_ut import ask_gpt
from utils.payments_ut import get_pay_link
from enums import PayType, HandlerKey


# старт запроса к гпт
async def send_main_menu(user: db.User = None, user_id: int = None, msg_id: int = None):
    text = await db.Text.get_text(HandlerKey.BACK_START.key)
    markup = kb.get_main_menu_kb()
    if msg_id:
        await bot.edit_message_text(
            chat_id=user_id, message_id=msg_id, text=text, reply_markup=markup, disable_web_page_preview=True
        )
    else:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup, disable_web_page_preview=True)


# старт запроса к гпт
async def send_gpt_start(user: db.User, msg_id: int = None):
    categories = await db.PromptCategory.get_all()
    # last_payment = await db.Payment.get_last_for_user(user.id)
    disallow = await db.DisallowCategory.get_disallow_list(user.tariff_id)
    text = await db.Text.get_text(HandlerKey.GPT_START_MSG.key)

    text = text.format(
        requests_remaining=user.requests_remaining,
        subscription_end=user.subscription_end_str()
    )

    markup = kb.get_prompt_categories_kb(categories, disallow)
    if msg_id:
        await bot.edit_message_text(chat_id=user.id, message_id=msg_id, text=text, reply_markup=markup)
    else:
        await bot.send_message(chat_id=user.id, text=text, reply_markup=markup)


# старт запроса к гпт
async def send_gpt_answer(
        user: db.User,
        user_prompt: str,
        prompt_id: int,
        state: FSMContext,
):

    try:
        text = await db.Text.get_text(HandlerKey.GPT_PROMPT_PRE_MSG.key)
        sent = await bot.send_message(chat_id=user.id, text=text)

        prompt = await db.Prompt.get_by_id(prompt_id)
        history = await db.Message.get_user_history(user_id=user.id, prompt_id=prompt.id)

        gpt_answer, usage = await ask_gpt(prompt=prompt, history=history, user_prompt=user_prompt)

        message_id = await db.Message.add(
            user_id=user.id,
            prompt_id=prompt.id,
            request=user_prompt,
            response=gpt_answer,
            prompt_tokens=usage.get('prompt_tokens', 0),
            completion_tokens=usage.get('completion_tokens', 0),
            time_answer=usage.get('time_answer'),
        )
        text_bottom = await db.Text.get_text(HandlerKey.GPT_PROMPT_MSG.key)
        text = (
            f'{gpt_answer}\n\n'
            f'{text_bottom}'
        )
        markup = kb.get_new_query_kb(message_id)
        try:
            await sent.edit_text(text=text, reply_markup=markup)
        except Exception as e:
            log_error(e)
            await sent.edit_text(text=text, parse_mode=None, reply_markup=markup)

        if user.tariff and not user.tariff.is_unlimited:
            await db.User.update(user_id=user.id, add_requests=-1)
            if user.requests_remaining == 1:
                await state.clear()
                text = await db.Text.get_text(HandlerKey.GPT_REQUESTS_OUT.key)
                await bot.send_message(chat_id=user.id, text=text, reply_markup=kb.get_start_payment_kb())

        return message_id

    except Exception as e:
        text = await db.Text.get_text(HandlerKey.GPT_PROMPT_ERROR_MSG.key)

        await bot.send_message(chat_id=user.id, text=text)
        log_error(e)


async def send_payment_start(user_id: int, user: db.User, msg_id: int = None):
    tariffs = await db.Tariff.get_all()

    text = ''
    for tariff in tariffs:
        text += f'{tariff.description}\n\n'

    text += await db.Text.get_text(HandlerKey.PAY_START_MSG.key)

    is_has_tariff = True if user.tariff else False
    with_requests = True if is_has_tariff and not user.tariff.is_unlimited else False

    markup = kb.get_payment_kb(tariffs, with_requests=with_requests)
    if msg_id:
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=text, reply_markup=markup)
    else:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup)


async def send_info_start(user_id: int, msg_id: int = None):
    text = await db.Text.get_text(HandlerKey.HELP_START_MSG.key,)

    info = await db.Info.get_all()

    markup = kb.get_info_menu_kb(info)
    if msg_id:
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=text, reply_markup=markup)
    else:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup)


async def send_balance_start(user: db.User, msg_id: int = None):
    text = await db.Text.get_text(HandlerKey.BALANCE_MSG.key)
    text = text.format(
        requests_remaining=user.requests_remaining,
        subscription_end=user.subscription_end_str(),
        tariff=user.tariff.name if user.tariff else 'Нет'
    )

    markup = kb.get_back_kb()
    if msg_id:
        await bot.edit_message_text(chat_id=user.id, message_id=msg_id, text=text, reply_markup=markup)
    else:
        await bot.send_message(chat_id=user.id, text=text, reply_markup=markup)


async def create_pay_link(user: db.User, tariff_id: int, pay_type: str, session_id: str, msg_id: int = None):
    try:
        if pay_type == PayType.TARIFF.value:
            tariff = await db.Tariff.get_by_id(tariff_id)
            text = await db.Text.get_text(HandlerKey.PAYMENT_URL_TARIFF.key)
            invoice = get_pay_link(
                user_id=user.id,
                tariff_id=tariff_id,
                email=user.email,
                amount=tariff.price,
                description=tariff.name,
                pay_type=pay_type,
                session_id=session_id
            )

            confirmation_url = invoice.confirmation.confirmation_url
            action = HandlerKey.PAYMENT_URL_TARIFF.key
            comment = f'Тариф {tariff.name}'

        else:
            request = await db.Request.get_by_id(tariff_id)
            text = await db.Text.get_text(HandlerKey.PAYMENT_URL_REQUEST.key)
            invoice = get_pay_link(
                user_id=user.id,
                tariff_id=tariff_id,
                email=user.email,
                amount=request.price,
                description=f'Покупка запросов {request.response_count}',
                pay_type=pay_type,
                session_id=session_id
            )

            confirmation_url = invoice.confirmation.confirmation_url
            action = HandlerKey.PAYMENT_URL_REQUEST.key
            comment = f'Покупка запросов {request.response_count}'

        if msg_id:
            await bot.edit_message_text(
                chat_id=user.id, message_id=msg_id, text=text, reply_markup=kb.get_payment_url_kb(confirmation_url))
        else:
            await bot.send_message(chat_id=user.id, text=text, reply_markup=kb.get_payment_url_kb(confirmation_url))

    except Exception as e:
        log_error(e)
        text = await db.Text.get_text(HandlerKey.PAYMENT_URL_ERROR.key)
        await bot.send_message(chat_id=user.id, text=text, reply_markup=kb.get_back_kb())

        action = HandlerKey.PAYMENT_URL_ERROR.key
        comment = f'{e}'[:255]

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=user.id,
        action=action,
        comment=comment,
        session=session_id
    )
