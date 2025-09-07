
from faststream.rabbit import (
    RabbitBroker,
    fastapi,
)

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


async def send_tg_code(data: CodeToTG,
                       broker: RabbitBroker
                       ) -> None:
    logger.debug(data)
    await broker.publish(data, tg_code_queue)


async def send_tg_notification(data: NotificationToTG,
                               broker: RabbitBroker
                               ) -> None:
    logger.debug(data)
    await broker.publish(data, notification_queue)
