
from fast_depends import Depends as Dp
from fast_depends import inject
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from shared.database import LanguageCodes
from shared.infrastructure import (
    RABBIT_URL,
    CodeToTG,
    tg_code_queue,
    notification_queue,
    NotificationToTG
)

from .bot import update_message
from .models import Notification
from .service import Service

broker = RabbitBroker(RABBIT_URL)
app = FastStream(broker)


@broker.subscriber(tg_code_queue)
async def handle_tg_code(data: CodeToTG) -> None:
    @inject
    async def _(id: int,
                data: str,
                service: Service = Dp(Service.depends)
                ) -> None:
        service.main_message.notifications.append(Notification(data))
        await service.save_main_message()
        service.notify = True
        await update_message(service.output())
    await _(data.tg_id, data.code)


@broker.subscriber(notification_queue)
async def handle_notification(data: NotificationToTG) -> None:
    @inject
    async def _(id: int,
                data: dict[LanguageCodes, str],
                service: Service = Dp(Service.depends)
                ) -> None:
        pass
    await _(data.tg_id, data.data)
