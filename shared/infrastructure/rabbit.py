
from faststream.rabbit import RabbitQueue
from pydantic import BaseModel

from shared.database import LanguageCodes
from shared.infrastructure import env_config

RABBIT_URL = f"amqp://{env_config.rabbit.user}:{env_config.rabbit.password}@{env_config.rabbit.ip}:{env_config.rabbit.port}/"


class CodeToTG(BaseModel):
    id: int
    username: str
    lang_code: LanguageCodes
    code: str


class NotificationToTG(BaseModel):
    data: dict[LanguageCodes, str]
    notify: bool = False


tg_code_queue = RabbitQueue(name="tg_code")
notification_queue = RabbitQueue(name="notification")
