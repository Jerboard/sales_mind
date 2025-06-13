from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import keyboards as kb
import utils as ut
import db
from settings import conf, log_error
from init import client_router, bot
from enums import CB, MenuCommand


@client_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_CATEGORY.value))
async def gpt_category(cb: CallbackQuery, state: FSMContext):
    await state.clear()

    _, category_id_str = cb.data.split(':')
    category_id = int(category_id_str)

    prompts = await db.Prompt.get_prompt_category(category_id)

    text = 'Выбирите промпт'
    await cb.message.edit_text(text, reply_markup=kb.get_prompt_kb(prompts))


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
    await state.clear()

    prompt = await db.Prompt.get_by_id(data.get('prompt_id'))

    if not prompt:
        await msg.answer(f'😅 Что-то пошло не так...\nПопробуйте повторить запрос /{MenuCommand.GPT.command}')
        log_error(f'gpt_prompt_msg, нет запроса', wt=False)
        return

    gpt_answer = await ut.ask_gpt(prompt, msg.text)

    await sent.edit_text(text=gpt_answer, reply_markup=kb.get_new_query_kb())


