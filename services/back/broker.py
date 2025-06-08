

from faststream.rabbit import RabbitBroker, fastapi

from config import settings

RABBIT_URL = f"amqp://{settings.rabbit_user}:{settings.rabbit_password}@{settings.rabbit_ip}:{settings.rabbit_port}/"

router = fastapi.RabbitRouter(RABBIT_URL)

def get_broker() -> RabbitBroker:
    return router.broker

async def send_message(data: dict, broker: RabbitBroker) -> None:
    await broker.publish(data, "message")
    