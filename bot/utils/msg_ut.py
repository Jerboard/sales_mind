from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import db
from init import bot
import keyboards as kb
from settings import conf, log_error
from utils.gpt_ut import ask_gpt
from enums import MenuCommand, HandlerKey


# старт запроса к гпт
async def send_main_menu(user: db.User = None, user_id: int = None, msg_id: int = None):
    text = await db.Text.get_text(HandlerKey.BACK_START.key)
    markup = kb.get_main_menu_kb()
    if msg_id:
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=text, reply_markup=markup)
    else:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup)


# старт запроса к гпт
async def send_gpt_start(user_id: int, msg_id: int = None):
    categories = await db.PromptCategory.get_all()
    text = await db.Text.get_text(HandlerKey.GPT_START_MSG.key)

    # text = '✅ Выбери нужный сценарий'
    markup = kb.get_prompt_categories_kb(categories)
    if msg_id:
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=text, reply_markup=markup)
    else:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup)


# старт запроса к гпт
async def send_gpt_answer(
        user_id: int,
        user_prompt: str,
        prompt_id: int,
):

    try:
        text = await db.Text.get_text(HandlerKey.GPT_PROMPT_PRE_MSG.key)
        sent = await bot.send_message(chat_id=user_id, text=text)

        prompt = await db.Prompt.get_by_id(prompt_id)
        history = await db.Message.get_user_history(user_id=user_id, prompt_id=prompt.id)

        gpt_answer, usage = await ask_gpt(prompt=prompt, history=history, user_prompt=user_prompt)

        message_id = await db.Message.add(
            user_id=user_id,
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

        return message_id

    except Exception as e:
        text = await db.Text.get_text(HandlerKey.GPT_PROMPT_ERROR_MSG.key)

        await bot.send_message(chat_id=user_id, text=text)
        log_error(e)


async def send_payment_start(user_id: int, msg_id: int = None):
    tariffs = await db.Tariff.get_all()

    text = ''
    for tariff in tariffs:
        text += f'{tariff.description}\n\n'

    text += await db.Text.get_text(HandlerKey.PAY_START_MSG.key)

    # text += f'<b>🎁 Попробовать бесплатно — 5 генераций для знакомства</b>'

    markup = kb.get_payment_kb(tariffs)
    if msg_id:
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=text, reply_markup=markup)
    else:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup)


async def send_info_start(user_id: int, msg_id: int = None):
    text = 'Выбери, что ты хочешь узнать 👇'
    text = await db.Text.get_text(HandlerKey.HELP_START_MSG.key,)

    info = await db.Info.get_all()

    markup = kb.get_info_menu_kb(info)
    if msg_id:
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=text, reply_markup=markup)
    else:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup)
