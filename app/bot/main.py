from telebot.async_telebot import AsyncTeleBot
import os
from dotenv import load_dotenv
import json

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = AsyncTeleBot(BOT_TOKEN)

with open("app/bot/static/ru_message_repository.json") as file:
    ru_messages = json.load(file)

with open("app/bot/static/en_message_repository.json") as file:
    en_messages = json.load(file)

with open("app/bot/static/templates.json") as file:
    templates = json.load(file)
