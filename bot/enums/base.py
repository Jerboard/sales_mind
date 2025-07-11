from enum import Enum


# Команды меню
class MenuCommand(Enum):
    START = ('start', '🔄 В начало')
    GPT = ('gpt', '💻 Создать запрос')
    PRICE = ('price', '💳 Тарифы и доступ')
    BALANCE = ('balance', '📊 Мой баланс')
    HELP = ('help', '⚙️ Помощь')

    def __init__(self, command, label):
        self.command = command
        self.label = label


# Команды меню
class Action(Enum):
    ADD = 'add'
    DEL = 'del'
    CONFIRM = 'confirm'
    BACK = 'back'
    NEW = 'new'
    EDIT = 'edit'


# ключи к функциям
class HandlerKey(Enum):
    COM_START = ('com_start', 'Основное меню (команда)')
    BACK_START = ('back_start', 'Основное меню (кнопка назад)')
    ACCEPT = ('accept', 'Принял политику')
    BALANCE_MSG = ('balance_msg', 'Посмотрел баланс (команда)')
    BALANCE_CB = ('balance_cb', 'Посмотрел баланс (кнопка)')

    GPT_START_MSG = ('gpt_start_msg', 'Перешёл в промпты (команда)')
    GPT_START_CB = ('gpt_start_cb', 'Перешёл в промпты (кнопка)')
    GPT_CATEGORY = ('gpt_category', 'Выбрал категорию')
    GPT_PROMPT = ('gpt_prompt', 'Выбрал промпт')

    GPT_PROMPT_PRE_MSG = ('gpt_prompt_pre_msg', '')
    GPT_PROMPT_MSG = ('gpt_prompt_msg', 'Запрос к гпт')
    GPT_PROMPT_ERROR_MSG = ('gpt_prompt_error_msg', '')

    GPT_REPEAT = ('gpt_repeat', 'Повтор запроса к гпт')
    GPT_RATE = ('gpt_rate', 'Поставил оценку')

    PAY_START_MSG = ('pay_start_msg', 'Тарифы (команда)')
    PAY_START_CB = ('pay_start_cb', 'Тарифы (кнопка)')
    PAYMENT_URL = ('payment_url', 'Получил ссылку на оплату')
    PAYMENT_TRY_USED_TRIAL = ('payment_used_trial', 'Повторно пробавл пробный период')
    PAYMENT_USE_TRIAL = ('PAYMENT_USE_TRIAL', 'Взял пробный период')
    PAYMENT_SUCCESS = ('payment_success', 'Успешная оплата')
    PAYMENT_DISALLOW = ('payment_disallow', 'Не хватает средств')

    HELP_START_MSG = ('gpt_help_msg', 'Помощь (команда)')
    HELP_START_CB = ('gpt_help_msg', 'Помощь (кнопка)')
    HELP_TEXT = ('help_text', 'Помощь текст')

    ERROR = ('error', 'Ошибка')
    BAN = ('ban', 'Бан попытка взаимодействия')
    EMPTY_REQUEST = ('empty_request', 'Запрос без статуса')

    def __init__(self, key, label):
        self.key = key
        self.label = label


# Кортеж кортежей для Django choices
HANDLER_KEY_CHOICES = tuple((member.key, member.label) for member in HandlerKey)
HANDLER_KEY_DICT = {member.key: member.label for member in HandlerKey}
