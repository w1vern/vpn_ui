
from fast_depends import Depends as Dp
from fast_depends import inject
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from shared.infrastructure import (
    RABBIT_URL,
    CodeToTG,
    tg_code_queue,
)

from .bot import update_message
from .models import Notification
from .services import Service

broker = RabbitBroker(RABBIT_URL)
app = FastStream(broker)


@broker.subscriber(tg_code_queue)
async def send_tg_code(data: CodeToTG
                       ) -> None:
    await tmp(data.tg_id, data.code)


@inject
async def tmp(id: int,
              code: str,
              service: Service = Dp(Service.depends)
              ) -> None:
    service.main_message.notifications.append(Notification(code))
    await service.save_main_message()
    service.notify = True
    await update_message(service.output())
