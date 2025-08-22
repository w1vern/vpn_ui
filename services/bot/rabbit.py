
from aiogram import Bot
from fast_depends import Depends as Dp
from fast_depends import inject
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from shared.infrastructure import (
    RABBIT_URL,
    CodeToTG,
    tg_code_queue,
)

from .bot import get_bot, update_message
from .models import Notification
from .services import Service

broker = RabbitBroker(RABBIT_URL)
app = FastStream(broker)


@broker.subscriber(tg_code_queue)
@inject
async def send_tg_code(data: CodeToTG,
                       service: Service = Dp(Service.depends)
                       ) -> None:
    # await bot.send_message(chat_id=data.tg_id, text=data.code)
    service.main_message.notifications.append(Notification(data.code))
    await service.__save_main_message()
    service.notify = True
    await update_message(service.__output())
