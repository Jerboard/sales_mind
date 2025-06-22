from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, Command

import keyboards as kb
import utils as ut
import db
from settings import conf, log_error
from init import main_router, bot
from enums import CB, MenuCommand, Action


@main_router.message(CommandStart())
async def com_start(msg: Message, state: FSMContext):
    await state.clear()

    await db.User.add(msg.from_user.id, msg.from_user.full_name, msg.from_user.username)

    text = '<a href="https://telegra.ph/Politika-ispolzovaniya-i-vozvrata--SalesMind-AI-06-22">Политика бота</a>'
    await msg.answer(text, reply_markup=kb.get_confirm_kb())

    # text = 'Приветствие срок подписки и подобное'
    # await msg.answer(text, reply_markup=kb.get_main_menu_kb())


@main_router.callback_query(lambda cb: cb.data.startswith(CB.COM_START.value))
async def back_start(cb: CallbackQuery, state: FSMContext):
    text = 'Приветствие срок подписки и подобное'
    await cb.message.edit_text(text, reply_markup=kb.get_main_menu_kb())


@main_router.callback_query(lambda cb: cb.data.startswith(CB.INFO.value))
async def info(cb: CallbackQuery, state: FSMContext):
    text = 'Инфо о проекте'
    await cb.message.edit_text(text, reply_markup=kb.get_back_kb())


@main_router.message(Command(MenuCommand.GPT.command))
async def gpt_start_msg(msg: Message, state: FSMContext):
    await ut.gpt_start(msg.from_user.id)


@main_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_START.value))
async def gpt_start_cb(cb: CallbackQuery, state: FSMContext):
    _, action = cb.data.split(':')

    if action == Action.EDIT.value:
        await ut.gpt_start(cb.from_user.id, msg_id=cb.message.message_id)
    else:
        await ut.gpt_start(cb.from_user.id)

