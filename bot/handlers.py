
from telebot.types import BotCommand, Message

from bot.commands import *
from bot.main import bot

commands = [
    BotCommand(command="/start", description="start bot")
]
bot.set_my_commands(commands)


@bot.message_handler(commands=["start"])
async def start(message: Message):
    await start_command(message)


""" 
@bot.message_handler(commands=["help"])
async def help(message: Message):
    await help_command(message)


@bot.message_handler(commands=["info"])
async def info(message: Message):
    await info_command(message)


@bot.message_handler(commands=["balance"])
async def balance(message: Message):
    await balance_command(message)


@bot.message_handler(commands=["start"])
async def installation(message: Message):
    await installation_command(message)
 """
""" 
# Главное меню
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Подменю 1"), KeyboardButton("Подменю 2"))
    return markup

# Подменю 1
def submenu_1():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Опция 1.1"), KeyboardButton("Опция 1.2"))
    markup.add(KeyboardButton("Назад"))
    return markup

# Подменю 2
def submenu_2():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Опция 2.1"), KeyboardButton("Опция 2.2"))
    markup.add(KeyboardButton("Назад"))
    return markup


# Обработчик команды /start
# @bot.message_handler(commands=["start"])
# async def start_command(message):
#     await bot.send_message(message.chat.id, "Добро пожаловать! Выберите опцию:", reply_markup=main_menu())

bot.register_message_handler(request_decorator(start_command), commands=["start"])

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
async def handle_message(message: Message):
    if message.text == "Подменю 1":
        await bot.send_message(message.chat.id, "Вы в подменю 1:", reply_markup=submenu_1())
    elif message.text == "Подменю 2":
        await bot.send_message(message.chat.id, "Вы в подменю 2:", reply_markup=submenu_2())
    elif message.text == "Назад":
        await bot.send_message(message.chat.id, "Вы вернулись в главное меню:", reply_markup=main_menu())
    elif message.text == "Опция 1.1":
        await bot.send_message(message.chat.id, "Вы выбрали Опцию 1.1")
    elif message.text == "Опция 1.2":
        await bot.send_message(message.chat.id, "Вы выбрали Опцию 1.2")
    elif message.text == "Опция 2.1":
        await bot.send_message(message.chat.id, "Вы выбрали Опцию 2.1")
    elif message.text == "Опция 2.2":
        await bot.send_message(message.chat.id, "Вы выбрали Опцию 2.2")
    else:
        await bot.send_message(message.chat.id, "Неизвестная команда. Выберите опцию из меню.")

 """
