
import os
from dotenv import load_dotenv
from fastapi import Depends
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitRouter, fastapi
import json
from app.site.token import TgCode

router = fastapi.RabbitRouter("amqp://guest:guest@localhost:5672/")

load_dotenv()

SECRET = os.getenv('SECRET')

def get_broker() -> RabbitBroker:
    return router.broker

async def send_message(data: dict, broker: RabbitBroker):
    await broker.publish(data, 'message')
    