

from faststream.rabbit import RabbitBroker, fastapi

from shared.config import env_config

RABBIT_URL = f"amqp://{env_config.rabbit.user}:{env_config.rabbit.password}@{env_config.rabbit.ip}:{env_config.rabbit.port}/"

router = fastapi.RabbitRouter(RABBIT_URL)

def get_broker() -> RabbitBroker:
    return router.broker

async def send_message(data: dict, broker: RabbitBroker) -> None:
    await broker.publish(data, "message")
    