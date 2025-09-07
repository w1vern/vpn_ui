
from faststream.rabbit import (
    RabbitBroker,
    fastapi,
)

from shared.database import LanguageCodes, User
from shared.infrastructure import (
    RABBIT_URL,
    CodeToTG,
    NotificationToTG,
    TgInfo,
    notification_queue,
    tg_code_queue
)

from .config import logger
from .schemas.user import UserSchema

router = fastapi.RabbitRouter(RABBIT_URL)


def get_broker() -> RabbitBroker:
    return router.broker


def get_tg_info(user: User | UserSchema) -> TgInfo:
    return TgInfo(id=user.telegram_id,
                  username=user.telegram_username,
                  lang_code=LanguageCodes(user.telegram_language_code))


async def send_tg_code(code: str,
                       user: User,
                       broker: RabbitBroker
                       ) -> None:
    data = CodeToTG(tg_info=get_tg_info(user), code=code)
    logger.debug(data)
    await broker.publish(data, tg_code_queue)


async def send_tg_notification(payload: dict[LanguageCodes, str],
                               user: UserSchema,
                               broker: RabbitBroker
                               ) -> None:
    data = NotificationToTG(tg_info=get_tg_info(user), data=payload)
    logger.debug(data)
    await broker.publish(data, notification_queue)
