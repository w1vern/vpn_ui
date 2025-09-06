
from faststream.rabbit import RabbitQueue
from pydantic import BaseModel

from shared.config import env_config
from shared.database import LanguageCodes

RABBIT_URL = f"amqp://{env_config.rabbit.user}:{env_config.rabbit.password}@{env_config.rabbit.ip}:{env_config.rabbit.port}/"


class CodeToTG(BaseModel):
    tg_id: int
    code: str

class NotificationToTG(BaseModel):
    tg_id: int
    data: dict[LanguageCodes, str]


tg_code_queue = RabbitQueue(name="tg_code")
notification_queue = RabbitQueue(name="notification")
