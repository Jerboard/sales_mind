from enum import Enum


# Команды меню
class CB(Enum):
    COM_START = 'com_start'
    ACCEPT = 'accept'
    BALANCE = 'balance'

    HELP_START = 'help_start'
    HELP_TEXT = 'help_text'

    PAYMENT_START = 'payment_start'
    PAYMENT_TARIFF = 'payment_tariff'
    PAYMENT_REQUESTS = 'payment_requests'

    GPT_START = 'gpt_start'
    GPT_CATEGORY = 'gpt_category'
    GPT_PROMPT = 'gpt_prompt'
    GPT_REPEAT = 'gpt_repeat'
    GPT_RATE = 'gpt_rate'

