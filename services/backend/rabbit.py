
from faststream.rabbit import RabbitBroker, fastapi

from shared.database import LanguageCodes, User
from shared.infrastructure import (
    RABBIT_URL,
    CodeToTG,
    NotificationToTG,
    notification_queue,
    tg_code_queue
)

from .config import logger

router = fastapi.RabbitRouter(RABBIT_URL)


def get_broker() -> RabbitBroker:
    return router.broker


async def send_tg_code(
    code: str,
    user: User,
    broker: RabbitBroker
) -> None:
    data = CodeToTG(
        id=user.telegram_id,
        username=user.telegram_username,
        lang_code=LanguageCodes(user.settings.language_code),
        code=code
    )
    logger.debug(data)
    await broker.publish(data, tg_code_queue)


async def send_tg_notification(
    payload: NotificationToTG,
    broker: RabbitBroker
) -> None:
    logger.debug(payload)
    await broker.publish(message=payload, queue=notification_queue)
