
from faststream.rabbit import (
    RabbitQueue,
)
from pydantic import BaseModel

from shared.config import (
    env_config,
)

RABBIT_URL = f"amqp://{env_config.rabbit.user}:{env_config.rabbit.password}@{env_config.rabbit.ip}:{env_config.rabbit.port}/"


class CodeToTG(BaseModel):
    tg_id: int
    code: str

tg_code_queue = RabbitQueue(name="tg_code")
