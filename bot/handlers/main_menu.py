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

    for i in msg.dict().items():
        print(i)

    await db.User.add(msg.from_user.id, msg.from_user.full_name, msg.from_user.username)

    user = await db.User.get_by_id(msg.from_user.id)

    # если принял правила то на главную, если нет то принимать
    if user.is_accepted:
        await ut.send_main_menu(user_id=user.id)
    else:
        text = ('Для взаимодействия с ботом необходимо ознакомиться и принять '
                '<a href="https://telegra.ph/Politika-ispolzovaniya-i-vozvrata--SalesMind-AI-06-22">'
                'политику использования</a>')
        await msg.answer(text, reply_markup=kb.get_confirm_kb())


@main_router.callback_query(lambda cb: cb.data.startswith(CB.COM_START.value))
async def back_start(cb: CallbackQuery, state: FSMContext):
    await ut.send_main_menu(user_id=cb.from_user.id, msg_id=cb.message.message_id)


@main_router.callback_query(lambda cb: cb.data.startswith(CB.ACCEPT.value))
async def accept(cb: CallbackQuery, state: FSMContext):
    await db.User.update(user_id=cb.from_user.id, is_accepted=True)

    await ut.send_main_menu(user_id=cb.from_user.id, msg_id=cb.message.message_id)


@main_router.message(Command(MenuCommand.GPT.command))
async def gpt_start_msg(msg: Message, state: FSMContext):
    await state.clear()

    user = await db.User.get_by_id(msg.from_user.id)

    # если принял правила то на главную, если нет то принимать
    if not user.is_accepted:
        text = ('Для взаимодействия с ботом необходимо ознакомиться и принять '
                '<a href="https://telegra.ph/Politika-ispolzovaniya-i-vozvrata--SalesMind-AI-06-22">'
                'политику использования</a>')
        await msg.answer(text, reply_markup=kb.get_confirm_kb())
        return

    await ut.send_gpt_start(msg.from_user.id)


@main_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_START.value))
async def gpt_start_cb(cb: CallbackQuery, state: FSMContext):
    _, action = cb.data.split(':')

    if action == Action.EDIT.value:
        await ut.send_gpt_start(cb.from_user.id, msg_id=cb.message.message_id)
    else:
        await ut.send_gpt_start(cb.from_user.id)


@main_router.message(Command(MenuCommand.PRICE.command))
async def gpt_price_msg(msg: Message, state: FSMContext):
    await state.clear()

    await ut.send_payment_start(user_id=msg.from_user.id)


@main_router.message(Command(MenuCommand.HELP.command))
async def gpt_help_msg(msg: Message, state: FSMContext):
    await state.clear()

    await ut.send_info_start(user_id=msg.from_user.id)
