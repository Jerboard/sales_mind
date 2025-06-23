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


@main_router.callback_query(lambda cb: cb.data.startswith(CB.INFO_START.value))
async def info(cb: CallbackQuery, state: FSMContext):
    text = 'Инфо о проекте'
    await cb.message.edit_text(text, reply_markup=kb.get_info_menu_kb())

@main_router.message(Command(MenuCommand.GPT.command))
async def gpt_start_msg(msg: Message, state: FSMContext):

    user = await db.User.get_by_id(msg.from_user.id)

    # если принял правила то на главную, если нет то принимать
    if not user.is_accepted:
        text = ('Для взаимодействия с ботом необходимо ознакомиться и принять '
                '<a href="https://telegra.ph/Politika-ispolzovaniya-i-vozvrata--SalesMind-AI-06-22">'
                'политику использования</a>')
        await msg.answer(text, reply_markup=kb.get_confirm_kb())
        return

    await ut.gpt_start(msg.from_user.id)


@main_router.callback_query(lambda cb: cb.data.startswith(CB.GPT_START.value))
async def gpt_start_cb(cb: CallbackQuery, state: FSMContext):
    _, action = cb.data.split(':')

    if action == Action.EDIT.value:
        await ut.gpt_start(cb.from_user.id, msg_id=cb.message.message_id)
    else:
        await ut.gpt_start(cb.from_user.id)


@main_router.callback_query(lambda cb: cb.data.startswith(CB.PAYMENT_START.value))
async def payment_start(cb: CallbackQuery, state: FSMContext):
    text = (
        '<b>🟢 Lite — 499 ₽ / мес</b>\n'
        '30 генераций в месяц  \n'
        '📞 Скрипты, 📩 Письма, 📈 KPI — всё включено \n '
        'Подходит для точечных задач\n\n'
        '<b>🔵 Pro — 999 ₽ / мес </b> \n'
        '100 генераций в месяц  \n'
        '+ приоритет в скорости  \n'
        '+ доступ ко всем разделам  \n'
        'Идеален для активных менеджеров\n'
        '<b>🟣 Expert — 1999 ₽ / мес  </b>\n'
        'Безлимит  \n'
        '+ индивидуальные шаблоны  \n'
        '+ early-доступ к новым функциям  \n'
        'Решение для команд и руководителей\n\n'
        '<b>🎁 Попробовать бесплатно — 5 генераций для знакомства</b>'
    )
    await cb.message.edit_text(text, reply_markup=kb.get_payment_kb())


@main_router.callback_query(lambda cb: cb.data.startswith(CB.PAYMENT_TARIFF.value))
async def payment_start(cb: CallbackQuery, state: FSMContext):
    text = (
        '<b>Формируем ссылку, отправляем на оплату</b>'
    )
    await cb.message.edit_text(text, reply_markup=kb.get_back_kb(cb=CB.PAYMENT_START.value))


