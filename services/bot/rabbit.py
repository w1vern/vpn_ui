

from aiogram import Bot
from faststream import (
    Depends,
    FastStream,
)
from faststream.rabbit import (
    RabbitBroker,
)

from shared.infrastructure import (
    RABBIT_URL,
    CodeToTG,
    tg_code_queue,
)

from .bot import get_bot

broker = RabbitBroker(RABBIT_URL)
app = FastStream(broker)


@broker.subscriber(tg_code_queue)
async def send_tg_code(data: CodeToTG, bot: Bot = Depends(get_bot)):
    await bot.send_message(chat_id=data.tg_id, text=data.code)
