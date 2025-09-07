
from fast_depends import Depends as Dp
from fast_depends import inject
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from shared.database import LanguageCodes
from shared.infrastructure import (
    RABBIT_URL,
    CodeToTG,
    NotificationToTG,
    notification_queue,
    tg_code_queue
)

from .bot import update_message
from .models import Notification, UserInfo
from .service import Service

broker = RabbitBroker(RABBIT_URL)
app = FastStream(broker)


@broker.subscriber(tg_code_queue)
async def handle_tg_code(data: CodeToTG) -> None:
    @inject
    async def _(user_info: UserInfo,
                data: str,
                service: Service = Dp(Service.depends)
                ) -> None:
        service.main_message.notifications.append(Notification(data))
        await service.save_main_message()
        service.notify = True
        await update_message(service.output())
    await _(UserInfo(data.tg_info.tg_id,
                     "",
                     LanguageCodes(data.tg_info.tg_lang_code)
                     ), data.code)


@broker.subscriber(notification_queue)
async def handle_notification(data: NotificationToTG) -> None:
    @inject
    async def _(user_info: UserInfo,
                data: dict[LanguageCodes, str],
                service: Service = Dp(Service.depends)
                ) -> None:
        pass
    await _(data.tg_id, data.data)
