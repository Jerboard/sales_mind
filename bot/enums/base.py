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


# Команды меню
class PayType(Enum):
    TARIFF = 'tariff'
    REQUEST = 'request'


PAY_TYPE_CHOICES = (
    (PayType.TARIFF.value, 'Тариф'),
    (PayType.REQUEST.value, 'Запросы')
)


# ключи к функциям
class HandlerKey(Enum):
    COM_START = ('com_start', 'Основное меню (команда)', True)
    BACK_START = ('back_start', 'Основное меню (кнопка назад)', True)
    ACCEPT = ('accept', 'Принял политику', True)
    BALANCE_MSG = ('balance_msg', 'Посмотрел баланс (команда)', False)
    BALANCE_CB = ('balance_cb', 'Посмотрел баланс (кнопка)', False)

    GPT_START_MSG = ('gpt_start_msg', 'Перешёл в промпты (команда)', True)
    GPT_START_CB = ('gpt_start_cb', 'Перешёл в промпты (кнопка)', False)
    GPT_CATEGORY = ('gpt_category', 'Выбрал категорию', True)
    GPT_PROMPT = ('gpt_prompt', 'Выбрал промпт', True)

    GPT_PROMPT_PRE_MSG = ('gpt_prompt_pre_msg', '', True)
    GPT_PROMPT_MSG = ('gpt_prompt_msg', 'Запрос к гпт', True)
    GPT_PROMPT_ERROR_MSG = ('gpt_prompt_error_msg', '', True)

    GPT_REPEAT = ('gpt_repeat', 'Повтор запроса к гпт', False)
    GPT_RATE = ('gpt_rate', 'Поставил оценку', True)

    PAY_START_MSG = ('pay_start_msg', 'Тарифы (команда)', True)
    PAY_START_CB = ('pay_start_cb', 'Тарифы (кнопка)', False)
    PAYMENT_URL_EMAIL = ('payment_url_email', 'Запрос почты', True)
    PAYMENT_ADD_EMAIL = ('payment_add_email', 'Добавил почту', True)
    PAYMENT_ADD_EMAIL_ERROR = ('payment_add_email_error', 'Ошибка ввода почты', True)
    PAYMENT_URL_TARIFF = ('payment_url', 'Получил ссылку на оплату тарифа', True)
    PAYMENT_URL_ERROR = ('payment_url_error', 'Ошибка получения ссылки', True)
    PAYMENT_URL_REQUEST_VIEW = ('payment_url_request_view', 'Посмотрел покупку запросов', True)
    PAYMENT_URL_REQUEST = ('payment_url_request', 'Получил ссылку на оплату запросов', True)
    PAYMENT_TRY_USED_TRIAL = ('payment_used_trial', 'Повторно пробавл пробный период', True)
    PAYMENT_USE_TRIAL = ('payment_use_trial', 'Взял пробный период', False)
    PAYMENT_SUCCESS = ('payment_success', 'Успешная оплата', True)
    PAYMENT_DISALLOW = ('payment_disallow', 'Не хватает средств', True)

    HELP_START_MSG = ('gpt_help_msg', 'Помощь (команда)', True)
    HELP_START_CB = ('gpt_help_msg', 'Помощь (кнопка)', True)
    HELP_TEXT = ('help_text', 'Помощь текст', False)

    ERROR = ('error', 'Ошибка', False)
    BAN = ('ban', 'Бан попытка взаимодействия', True)
    EMPTY_REQUEST = ('empty_request', 'Запрос без статуса', True)

    SEND_NOTICE_1 = ('send_notice_1', 'Напоминание за 2 дня', True)
    SEND_NOTICE_2 = ('send_notice_2', 'Закончилась подписка', True)

    def __init__(self, key, label, with_text):
        self.key = key
        self.label = label
        self.with_text = with_text


# Кортеж кортежей для Django choices
HANDLER_KEY_CHOICES = tuple((member.key, member.label) for member in HandlerKey)
HANDLER_KEY_DICT = {member.key: member.label for member in HandlerKey}
