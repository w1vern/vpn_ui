
from aiogram import Bot, Dispatcher

from .handlers import router
from .lifecycle import register_lifecycle
from config import settings


async def main() -> None:
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.include_router(router)
    register_lifecycle(dp, bot)

    await dp.start_polling(bot)