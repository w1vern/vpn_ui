from telebot.async_telebot import AsyncTeleBot
from telebot import telebot
import os
from dotenv import load_dotenv
import json

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception = None):
        print(exception)

bot = AsyncTeleBot(BOT_TOKEN, exception_handler=ExceptionHandler)

with open("app/bot/static/ru_message_repository.json", encoding="utf-8") as file:
    ru_messages = json.load(file)

with open("app/bot/static/en_message_repository.json", encoding="utf-8") as file:
    en_messages = json.load(file)

with open("app/bot/static/templates.json", encoding="utf-8") as file:
    templates = json.load(file)


