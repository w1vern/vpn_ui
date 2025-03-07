

from faststream import Depends, FastStream
from faststream.rabbit import RabbitBroker
from telebot.async_telebot import AsyncTeleBot

from bot.di_implementation import get_bot

from config import settings


RABBIT_URL = f"amqp://{settings.rabbit_user}:{settings.rabbit_password}@{settings.rabbit_ip}:{settings.rabbit_port}/"


broker = RabbitBroker(RABBIT_URL)

app = FastStream(broker)

@broker.subscriber("message")
async def message_consumer(body: dict, bot: AsyncTeleBot = Depends(get_bot)):
    await bot.send_message(chat_id=body["tg_id"], text=body["text"])
