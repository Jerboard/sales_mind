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
    info = await db.Info.get_all()
    await cb.message.edit_text(text, reply_markup=kb.get_info_menu_kb(info))


@main_router.callback_query(lambda cb: cb.data.startswith(CB.INFO_TEXT.value))
async def payment_start(cb: CallbackQuery, state: FSMContext):
    _, info_id_str, back = cb.data.split(':')
    info_id = int(info_id_str)

    info = await db.Info.get_by_id(info_id)
    await cb.message.edit_text(
        info.description,
        reply_markup=kb.get_back_kb(cb=back)
    )


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



@main_router.callback_query(lambda cb: cb.data.startswith(CB.INFO_DEMO.value))
async def info_demo(cb: CallbackQuery, state: FSMContext):
    text = (
        '''🧠 Что я умею:

📞 Генерировать скрипты звонков  
— Холодные, повторные, апсейлы, диагностика

📩 Создавать письма и follow-up  
— Первый контакт, напоминания, ответы на тишину

📈 Строить KPI и планы  
— Месячные цели, активность, показатели команды

👥 Помогать с наймом  
— Вакансии, тестовые задания, скрипты интервью

🧠 Отвечать на возражения  
— Дорого, нет времени, «мы подумаем» — всё решаемо

📋 Давать чек-листы  
— Перед звонком, после встречи, перед сделкой

⚡️ Работать мгновенно и без суеты  
— Просто опиши задачу — остальное сделаю я.
'''
    )
    await cb.message.edit_text(text, reply_markup=kb.get_back_kb())


