from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, Command

import keyboards as kb
import utils as ut
import db
from settings import conf, log_error
from init import main_router, bot
from enums import CB, MenuCommand, Action, HandlerKey


@main_router.message(CommandStart())
async def com_start(msg: Message, state: FSMContext, session_id: str):
    await state.clear()

    source = msg.text.split('=')[-1] if msg.text.split('=')[-1] != f'/{MenuCommand.START.command}' else None
    print(source)

    await db.User.add(msg.from_user.id, msg.from_user.full_name, msg.from_user.username, source=source)
    user = await db.User.get_by_id(msg.from_user.id)

    # если принял правила то на главную, если нет то принимать
    if user.is_accepted:
        await ut.send_main_menu(user_id=user.id)
    else:
        text = await db.Text.get_text(HandlerKey.COM_START.key)
        await msg.answer(text, reply_markup=kb.get_confirm_kb())

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=msg.from_user.id,
        action=HandlerKey.COM_START.key,
        session=session_id
    )


@main_router.callback_query(lambda cb: cb.data.startswith(CB.COM_START.value))
async def back_start(cb: CallbackQuery, state: FSMContext, session_id: str):
    await ut.send_main_menu(user_id=cb.from_user.id, msg_id=cb.message.message_id)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.BACK_START.key,
        session=session_id
    )


@main_router.callback_query(lambda cb: cb.data.startswith(CB.ACCEPT.value))
async def accept(cb: CallbackQuery, state: FSMContext, session_id: str):
    await db.User.update(user_id=cb.from_user.id, is_accepted=True)

    await ut.send_main_menu(user_id=cb.from_user.id, msg_id=cb.message.message_id)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.ACCEPT.key,
        session=session_id
    )


@main_router.message(Command(MenuCommand.GPT.command))
async def gpt_start_msg(msg: Message, state: FSMContext, session_id: str, user: db.User):
    await state.clear()

    # user = await db.User.get_by_id(msg.from_user.id)

    # если принял правила то на главную, если нет то принимать
    if not user.is_accepted:
        text = await db.Text.get_text(HandlerKey.COM_START.key)
        await msg.answer(text, reply_markup=kb.get_confirm_kb())
        return

    await ut.send_gpt_start(user)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=msg.from_user.id,
        action=HandlerKey.GPT_START_MSG.key,
        session=session_id
    )


@main_router.message(Command(MenuCommand.PRICE.command))
async def pay_start_msg(msg: Message, state: FSMContext, session_id: str, user: db.User):
    await state.clear()

    await ut.send_payment_start(user_id=msg.from_user.id, user=user)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=msg.from_user.id,
        action=HandlerKey.PAY_START_MSG.key,
        session=session_id
    )


@main_router.message(Command(MenuCommand.HELP.command))
async def gpt_help_msg(msg: Message, state: FSMContext, session_id: str):
    await state.clear()

    await ut.send_info_start(user_id=msg.from_user.id)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=msg.from_user.id,
        action=HandlerKey.HELP_START_MSG.key,
        session=session_id
    )


@main_router.message(Command(MenuCommand.BALANCE.command))
async def gpt_balance_msg(msg: Message, state: FSMContext, session_id: str, user: db.User):
    await state.clear()

    await ut.send_balance_start(user=user)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=msg.from_user.id,
        action=HandlerKey.BALANCE_MSG.key,
        session=session_id
    )


@main_router.callback_query(lambda cb: cb.data.startswith(CB.BALANCE.value))
async def gpt_balance_cb(cb: CallbackQuery, state: FSMContext, session_id: str, user: db.User):
    await state.clear()

    await ut.send_balance_start(user=user, msg_id=cb.message.message_id)

    # сохраняем действия пользователя
    await db.LogsUser.add(
        user_id=cb.from_user.id,
        action=HandlerKey.BALANCE_CB.key,
        session=session_id
    )
