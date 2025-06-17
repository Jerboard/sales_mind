from enum import Enum


# Команды меню
class CB(Enum):
    COM_START = 'com_start'
    INFO = 'info'
    PAYMENT_START = 'payment_start'

    GPT_START = 'gpt_start'
    GPT_CATEGORY = 'gpt_category'
    GPT_PROMPT = 'gpt_prompt'
    GPT_RATE = 'gpt_rate'

