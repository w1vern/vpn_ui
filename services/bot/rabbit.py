
from aiogram import Bot
from fast_depends import inject, Depends as Dp
from faststream import (
    Depends,
    FastStream,
)
from faststream.rabbit import RabbitBroker

from .depends import Notification
from .handlers import update_inline

from .services import Service
from shared.infrastructure import (
    RABBIT_URL,
    CodeToTG,
    tg_code_queue,
)

from .bot import get_bot

broker = RabbitBroker(RABBIT_URL)
app = FastStream(broker)


@broker.subscriber(tg_code_queue)
@inject
async def send_tg_code(data: CodeToTG,
                       bot: Bot = Depends(get_bot),
                       service: Service = Dp(Service.depends)
                       ) -> None:
    # await bot.send_message(chat_id=data.tg_id, text=data.code)
    service.main_message.notifications.append(Notification(data.code))
    await service.__save_main_message()
    await update_inline(service.__output())
