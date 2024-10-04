
import asyncio

from telebot.async_telebot import AsyncTeleBot
import os

from dotenv import load_dotenv

BOT_TOKEN = load_dotenv("BOT_TOKEN")

bot = AsyncTeleBot('BOT_TOKEN')


