
from faststream import FastStream, Depends
from faststream.rabbit import RabbitBroker

from bot.di_implementation import get_bot
from telebot.async_telebot import AsyncTeleBot

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")

app = FastStream(broker)

@broker.subscriber("message")
async def message_consumer(body: dict, bot: AsyncTeleBot = Depends(get_bot)):
    await bot.send_message(chat_id=body["tg_id"], text=body["text"])
