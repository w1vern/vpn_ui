

import os
from dotenv import load_dotenv
from fastapi import Depends
from faststream.rabbit import RabbitBroker, fastapi

load_dotenv()

RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD")
RABBIT_IP = os.getenv("RABBIT_IP")
RABBIT_PORT = os.getenv("RABBIT_PORT")


if RABBIT_USER is None or RABBIT_PASSWORD is None or RABBIT_IP is None or RABBIT_PORT is None:
    raise Exception("RABBIT_USER or RABBIT_PASSWORD or RABBIT_IP or RABBIT_PORT is not set")

RABBIT_URL = f"amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_IP}:{RABBIT_PORT}/"



router = fastapi.RabbitRouter(RABBIT_URL)

def get_broker() -> RabbitBroker:
    return router.broker

async def send_message(data: dict, broker: RabbitBroker):
    await broker.publish(data, "message")
    