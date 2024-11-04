

from fastapi import Depends
from faststream.rabbit import RabbitBroker, fastapi

router = fastapi.RabbitRouter("amqp://guest:guest@localhost:5672/")

def get_broker() -> RabbitBroker:
    return router.broker

async def send_message(data: dict, broker: RabbitBroker):
    await broker.publish(data, "message")
    