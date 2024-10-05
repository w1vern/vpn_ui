
from app.bot.__main__ import bot
from app.bot.commands import *

from telebot.types import Message


@bot.message_handler(commands=['start'])
async def start(message: Message):
    await start_command(message)


@bot.message_handler(commands=['help'])
async def help(message):
    

@bot.message_handler(commands=['info'])
async def info(message):
    pass

@bot.message_handler(commands=['balance'])
async def balance(message):
    pass

@bot.message_handler(commands=['start'])
async def start(message):
    pass

@bot.message_handler(commands=['start'])
async def start(message):
    pass


    
