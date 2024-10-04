
from app.bot.main import bot
from app.bot.commands import *

from telebot.types import Message


@bot.message_handler(commands=['start'])
async def start(message: Message):
    await start_command(message)


@bot.message_handler(commands=['help'])
async def start(message):
    

@bot.message_handler(commands=['info'])
async def start(message):
    pass

@bot.message_handler(commands=[''])
async def start(message):
    pass

@bot.message_handler(commands=['start'])
async def start(message):
    pass

@bot.message_handler(commands=['start'])
async def start(message):
    pass


    
