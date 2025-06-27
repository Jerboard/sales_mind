from enum import Enum


# Команды меню
class MenuCommand(Enum):
    START = ('start', '🔄 В начало')
    GPT = ('gpt', '💻 Создать запрос')
    PRICE = ('price', '💳 Тарифы и доступ')
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

