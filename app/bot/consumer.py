import json
import pika

from app.bot.di_implementation import inject, di
from telebot.async_telebot import AsyncTeleBot

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

queue_name='message_queue'

channel.queue_declare(queue=queue_name)

@inject(di)
def message_consumer(ch, method, properties, body, bot: AsyncTeleBot):
    message = body.decode()
    dict = json.loads(message)
    bot.send_message(chat_id=dict['tg_id'], text=dict['text'])


channel.basic_consume(queue=queue_name, on_message_callback=message_consumer, auto_ack=True)
channel.start_consuming()