from enum import Enum


# Команды меню
class CB(Enum):
    COM_START = 'com_start'
    ACCEPT = 'accept'

    INFO_START = 'info_start'
    INFO_TEXT = 'info_text'
    INFO_DEMO = 'info_demo'

    PAYMENT_START = 'payment_start'
    PAYMENT_TARIFF = 'payment_tariff'

    GPT_START = 'gpt_start'
    GPT_CATEGORY = 'gpt_category'
    GPT_PROMPT = 'gpt_prompt'
    GPT_RATE = 'gpt_rate'

