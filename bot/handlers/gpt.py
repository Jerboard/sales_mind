from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.parse_mode import ParseMode

import re
import logging
import time
import os

import keyboards as kb
import utils as ut
import db
from settings import conf, log_error
from init import client_router, bot
from enums import CB, HandlerKey, Action


logger = logging.getLogger('gpt_time_logs')
gpt_log_file = os.path.join('logs', f'time_gpt.log')
gpt_handler = logging.FileHandler(gpt_log_file, encoding='utf-8')
gpt_handler.setLevel(logging.WARNING)
logger.addHandler(gpt_handler)
logger.setLevel(logging.WARNING)


@client_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_START.value))
async def gpt_start_cb(cb: CallbackQuery, state: FSMContext, session_id: str, user: db.User):
    _, action = cb.data.split(':')

    if action == Action.EDIT.value:
        await ut.send_gpt_start(user, msg_id=cb.message.message_id)
    else:
        await ut.send_gpt_start(user)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.GPT_START_CB.key,
        session=session_id
    )


@client_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_CATEGORY.value))
async def gpt_category(cb: CallbackQuery, state: FSMContext, session_id: str, user: db.User):
    await state.clear()
    _, category_id_str = cb.data.split(':')
    category_id = int(category_id_str)

    prompts = await db.Prompt.get_prompt_category(category_id)
    category = await db.PromptCategory.get_by_id(category_id)

    text = await db.Text.get_text(HandlerKey.GPT_CATEGORY.key)
    text = text.format(
        category=category.name,
        requests_remaining=user.requests_remaining,
        subscription_end=user.subscription_end_str()
    )
    markup = kb.get_prompt_kb(prompts)
    await cb.message.edit_text(text, reply_markup=markup)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.GPT_CATEGORY.key,
        comment=f'{category.name}',
        session=session_id
    )


@client_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_PROMPT.value))
async def gpt_prompt(cb: CallbackQuery, state: FSMContext, session_id: str, user: db.User):

    _, prompt_id_str = cb.data.split(':')
    prompt_id = int(prompt_id_str)

    # prompt = await db.Prompt.get_by_id(prompt_id)
    prompt = await db.Prompt.get_prompt_with_category(prompt_id)

    await state.set_state(CB.GPT_PROMPT.value)
    await state.update_data(
        data={
            'msg_id': cb.message.message_id,
            'prompt_id': prompt_id,
            'prompt': prompt,
        }
    )
    text = await db.Text.get_text(HandlerKey.GPT_PROMPT.key)
    # text = text.format(category=prompt.prompt_category.name, prompt_name=prompt.name)
    text = text.format(
        category=prompt.prompt_category.name,
        prompt_name=prompt.name,
        requests_remaining=user.requests_remaining,
        subscription_end=user.subscription_end_str()
    )
    text += f'\n\n{prompt.hint}'

    await cb.message.edit_text(text, reply_markup=kb.get_back_kb(cb=CB.GPT_CATEGORY.value, value=prompt.category_id))

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.GPT_PROMPT.key,
        comment=f'{prompt.name}',
        session=session_id
    )


# сам запрос
@client_router.message(StateFilter(CB.GPT_PROMPT.value))
async def gpt_prompt_msg(msg: Message, state: FSMContext, session_id: str, user: db.User):
    t0 = time.perf_counter()
    data = await state.get_data()

    message_id = await ut.send_gpt_answer(
        user=user,
        user_prompt=msg.text,
        prompt_id=data.get('prompt_id')
    )

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=msg.from_user.id,
        action=HandlerKey.GPT_PROMPT_MSG.key,
        msg_id=message_id,
        session=session_id
    )

    logger.warning(f'{message_id}: {time.perf_counter() - t0:.2f}')


@client_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_REPEAT.value))
async def gpt_repeat(cb: CallbackQuery, state: FSMContext, session_id: str, user: db.User):
    t0 = time.perf_counter()

    _, answer_id_str = cb.data.split(':')
    answer_id = int(answer_id_str)

    answer = await db.Message.get_by_id(answer_id)
    prompt = 'Предложи ещё варианты по предидущему запросу'

    message_id = await ut.send_gpt_answer(
        user=user,
        user_prompt=prompt,
        prompt_id=answer.prompt_id
    )

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.GPT_REPEAT.key,
        msg_id=message_id,
        session=session_id
    )
    logger.warning(f'{message_id}: {time.perf_counter() - t0:.2f} repeat')


@client_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_RATE.value))
async def gpt_rate(cb: CallbackQuery, state: FSMContext, session_id: str):
    _, msg_id_str, rate_str = cb.data.split(':')
    msg_id = int(msg_id_str)
    rate = bool(int(rate_str))

    answer_rate = '👍' if rate else '👎'

    text = cb.message.text
    # 1. Срезаем старую оценку (если она была) вместе с лишними \n
    #    – убираем:   «\n\n👍»  или  «\n\n👎»  или просто «👍/👎» на самом хвосте
    text = re.sub(r'(?:\n*\s*\n)?[👍👎]$', '', text).rstrip()

    # 2. Приписываем свежую
    text = f'{text}\n\n{answer_rate}'
    await db.Message.update(message_id=msg_id, is_like=rate)

    text_answer = await db.Text.get_text(HandlerKey.GPT_RATE.key)
    await cb.answer(text_answer)

    try:
        await cb.message.edit_text(
            text=text,
            entities=cb.message.entities,
            parse_mode=None,
            reply_markup=kb.get_new_query_kb(msg_id)
        )
    except Exception as e:
        log_error(e)
        answer_rate += f' ❗️Ошибка: {e}'

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.GPT_RATE.key,
        comment=answer_rate,
        msg_id=msg_id,
        session=session_id
    )
