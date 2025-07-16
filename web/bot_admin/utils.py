from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from .models import Text, LogsUser
from web.settings import bot
from enums import CB, Action


def get_success_pay_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text='🚀 Начать работать',
            callback_data=f'{CB.GPT_START.value}:{Action.EDIT.value}'
        )
    )
    return kb


def get_start_payment_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text='💳 Тарифы и доступ',
            callback_data=f'{CB.PAYMENT_START.value}'
        )
    )
    return kb


def send_notice(user_id: int, key: str):
    text = Text.get_by_key(key)
    print(text)

    bot.send_message(chat_id=user_id, text=text.text, reply_markup=get_start_payment_kb())

    # сохраняем действия пользователя
    LogsUser.add(user_id=user_id, action=key)
