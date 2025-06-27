from aiogram.types import Message, CallbackQuery

import db
from init import bot
import keyboards as kb


# старт запроса к гпт
async def send_main_menu(user: db.User = None, user_id: int = None, msg_id: int = None):
    text = ('🤖 Привет!\n'
            'Я — SalesMind AI, твой ассистент по продажам.\n'
            'Скрипты, письма, KPI, найм — всё за секунды.\n\n'
            '🎯 Хочешь видеть быть в курсе обновлений, реальных кейсов работы с ботом и новостей?\n'
            'Подписывайся на канал 👉 @SalesMindAI\n\n'
            'Выбирай, что нужно 👇'
            )
    markup = kb.get_main_menu_kb()
    if msg_id:
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=text, reply_markup=markup)
    else:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup)


# старт запроса к гпт
async def gpt_start(user_id: int, msg_id: int = None):
    categories = await db.PromptCategory.get_all()
    text = '✅ Выбери нужный сценарий'
    markup = kb.get_prompt_categories_kb(categories)
    if msg_id:
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=text, reply_markup=markup)
    else:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup)


