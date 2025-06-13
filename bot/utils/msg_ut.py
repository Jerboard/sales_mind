from aiogram.types import Message, CallbackQuery

import db
from init import bot
import keyboards as kb


# старт запроса к гпт
async def gpt_start(user_id: int, msg_id: int = None):
    categories = await db.PromptCategory.get_all()
    text = 'Выбирите подходящий сценарий'
    markup = kb.get_prompt_categories_kb(categories)
    if msg_id:
        await bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=text, reply_markup=markup)
    else:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup)


