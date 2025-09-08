
from fast_depends import Depends, inject
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from shared.database import LanguageCodes
from shared.infrastructure import (
    RABBIT_URL,
    CodeToTG,
    NotificationToTG,
    TgInfo,
    notification_queue,
    tg_code_queue
)

from .bot import update_message
from .models import Notification, UserInfo
from .service import Service

broker = RabbitBroker(RABBIT_URL)
app = FastStream(broker)


async def handler(text: str,
                  tg_info: TgInfo
                  ) -> None:
    @inject
    async def _(text: str,
                user_info: UserInfo,
                service: Service = Depends(Service.depends)
                ) -> None:
        service.main_message.notifications.append(Notification(text))
        await service.save_main_message()
        service.notify = True
        await update_message(service.output())
    await _(text, UserInfo(tg_info.id, tg_info.username, tg_info.lang_code))


@broker.subscriber(tg_code_queue)
async def handle_tg_code(data: CodeToTG) -> None:
    await handler(data.code, data.tg_info)


@broker.subscriber(notification_queue)
async def handle_notification(data: NotificationToTG) -> None:
    text = data.data.get(data.tg_info.lang_code, LanguageCodes.en.value)
    await handler(text, data.tg_info)
