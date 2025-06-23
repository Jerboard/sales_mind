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


@client_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_CATEGORY.value))
async def gpt_category(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    _, category_id_str = cb.data.split(':')
    category_id = int(category_id_str)

    prompts = await db.Prompt.get_prompt_category(category_id)

    text = 'Выбирите сценарий'
    markup = kb.get_prompt_kb(prompts)

    await cb.message.edit_text(text, reply_markup=markup)

    # if action == Action.EDIT.value:
    # else:
    #     await cb.message.answer(text, reply_markup=markup)


@client_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_PROMPT.value))
async def gpt_prompt(cb: CallbackQuery, state: FSMContext):
    await state.clear()

    _, prompt_id_str = cb.data.split(':')
    prompt_id = int(prompt_id_str)

    prompt = await db.Prompt.get_by_id(prompt_id)

    await state.set_state(CB.GPT_PROMPT.value)
    await state.update_data(
        data={
            'msg_id': cb.message.message_id,
            'prompt_id': prompt_id,
            'prompt': prompt,
        }
    )
    text = (
        f'Составте запрос\n\n'
        f'{prompt.hint}'
    )
    await cb.message.edit_text(text, reply_markup=kb.get_back_kb(cb=CB.GPT_CATEGORY.value, value=prompt.category_id))


# сам запрос
@client_router.message(StateFilter(CB.GPT_PROMPT.value))
async def gpt_prompt_msg(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        await msg.answer(f'😅 Что-то пошло не так...\nПопробуйте повторить запрос /{MenuCommand.GPT.command}')
        log_error(f'gpt_prompt_msg, нет состаяния', wt=False)
        return

    sent = await msg.answer('Думаю...')

    data = await state.get_data()
    # await state.clear()

    prompt = await db.Prompt.get_by_id(data.get('prompt_id'))
    if not prompt:
        await msg.answer(f'😅 Что-то пошло не так...\nПопробуйте повторить запрос /{MenuCommand.GPT.command}')
        log_error(f'gpt_prompt_msg, нет запроса', wt=False)
        return

    history = await db.Message.get_user_history(user_id=msg.from_user.id, prompt_id=prompt.id)
    gpt_answer, usage = await ut.ask_gpt(prompt=prompt, history=history, user_prompt=msg.text)

    message_id = await db.Message.add(
        user_id=msg.from_user.id,
        prompt_id=prompt.id,
        request=msg.text,
        response=gpt_answer,
        prompt_tokens=usage.get('prompt_tokens', 0),
        completion_tokens=usage.get('completion_tokens', 0),
        time_answer=usage.get('time_answer'),
    )
    try:
        await sent.edit_text(text=gpt_answer, reply_markup=kb.get_new_query_kb(message_id))
    except Exception as e:
        log_error(e)
        await sent.edit_text(text=gpt_answer, parse_mode=None, reply_markup=kb.get_new_query_kb(message_id))



@client_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_RATE.value))
async def gpt_rate(cb: CallbackQuery, state: FSMContext):
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
    await cb.answer('Оценка поставлена')
    try:
        await cb.message.edit_text(
            text=text,
            entities=cb.message.entities,
            parse_mode=None,
            reply_markup=kb.get_new_query_kb(msg_id)
        )
    except:
        pass
