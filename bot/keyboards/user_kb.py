from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

import db
from settings import conf
from enums import CB, Action


# Кнопки подписаться на канал
def get_back_kb(cb: str = CB.COM_START.value, value: str = Action.BACK.value) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=f'{cb}:{value}')
    return kb.adjust(1).as_markup()


# Кнопки подписаться на канал
def get_confirm_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='✅ Принять', callback_data=f'{CB.ACCEPT.value}')
    return kb.adjust(1).as_markup()


# Кнопки подписаться на канал
def get_main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🧠 Что я умею', callback_data=f'{CB.INFO_TEXT.value}:1:com_start')
    kb.button(text='💳 Тарифы и доступ', callback_data=f'{CB.PAYMENT_START.value}')
    kb.button(text='🚀 Начать работать', callback_data=f'{CB.GPT_START.value}:{Action.EDIT.value}')
    kb.button(text='⚙️ Помощь', callback_data=f'{CB.INFO_START.value}')

    return kb.adjust(1).as_markup()


# Выбор категории
def get_prompt_categories_kb(categories: list[db.PromptCategory]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for category in categories:
        kb.button(text=category.name, callback_data=f'{CB.GPT_CATEGORY.value}:{category.id}')
    kb.button(text='🔙 Назад', callback_data=f'{CB.COM_START.value}')
    return kb.adjust(1).as_markup()


# Промпта
def get_prompt_kb(prompts: list[db.Prompt]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for prompt in prompts:
        kb.button(text=prompt.name, callback_data=f'{CB.GPT_PROMPT.value}:{prompt.id}')
    kb.button(text='🔙 Назад', callback_data=f'{CB.GPT_START.value}:{Action.EDIT.value}')
    return kb.adjust(1).as_markup()


# Кнопки подписаться на канал
def get_new_query_kb(message_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='👍', callback_data=f'{CB.GPT_RATE.value}:{message_id}:1')
    kb.button(text='👎', callback_data=f'{CB.GPT_RATE.value}:{message_id}:0')
    kb.button(text='🔄 Попробовать другой вариант', callback_data=f'{CB.GPT_REPEAT.value}:{message_id}')
    kb.button(text='💻 Выбрать другой сценарий', callback_data=f'{CB.GPT_START.value}:{Action.NEW.value}')

    return kb.adjust(2, 1).as_markup()


# Основные тарифы
def get_payment_kb(tariffs: list[db.Tariff]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for tariff in tariffs:
        kb.button(text=tariff.name, callback_data=f'{CB.PAYMENT_TARIFF.value}:{tariff.id}')
    kb.button(text='⬅️ Назад', callback_data=f'{CB.COM_START.value}')

    return kb.adjust(1).as_markup()


# Инфо кнопки
def get_info_menu_kb(info: list[db.Info]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for i in info:
        kb.button(text=i.name, callback_data=f'{CB.INFO_TEXT.value}:{i.id}:{CB.INFO_START.value}')
    kb.button(text='⬅️ Назад', callback_data=f'{CB.COM_START.value}')

    return kb.adjust(1).as_markup()
