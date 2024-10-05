from telebot.async_telebot import AsyncTeleBot
import os
from dotenv import load_dotenv
import json

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = AsyncTeleBot('BOT_TOKEN')

static_messages = json.loads("./static/messages.json")