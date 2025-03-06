
import os
from dotenv import load_dotenv
from faststream import Depends, FastStream
from faststream.rabbit import RabbitBroker
from telebot.async_telebot import AsyncTeleBot

from bot.di_implementation import get_bot

load_dotenv()

RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD")
RABBIT_IP = os.getenv("RABBIT_IP")
RABBIT_PORT = os.getenv("RABBIT_PORT")


if RABBIT_USER is None or RABBIT_PASSWORD is None or RABBIT_IP is None or RABBIT_PORT is None:
    raise Exception("RABBIT_USER or RABBIT_PASSWORD or RABBIT_IP or RABBIT_PORT is not set")

RABBIT_URL = f"amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_IP}:{RABBIT_PORT}/"

broker = RabbitBroker(RABBIT_URL)

app = FastStream(broker)

@broker.subscriber("message")
async def message_consumer(body: dict, bot: AsyncTeleBot = Depends(get_bot)):
    await bot.send_message(chat_id=body["tg_id"], text=body["text"])
