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
def get_main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🧠 Что я умею', callback_data=f'{CB.INFO.value}')
    kb.button(text='💳 Оплата', callback_data=f'{CB.PAYMENT_START.value}')
    kb.button(text='💻 Отправить запрос', callback_data=f'{CB.GPT_START.value}')

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
    kb.button(text='🔙 Назад', callback_data=f'{CB.GPT_START.value}')
    return kb.adjust(1).as_markup()


# Кнопки подписаться на канал
def get_new_query_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='💻 Отправить новый запрос', callback_data=f'{CB.GPT_START.value}')

    return kb.adjust(1).as_markup()

'''
🧠 Что я умею
📞 Скрипты звонков
📩 Письма клиентам
📈 KPI / тесты
💼 Найм / развитие
🧾 Подписка и тарифы
'''