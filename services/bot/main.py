
from aiogram import Bot, Dispatcher

from config import settings

from .handlers import router
from .lifecycle import register_lifecycle


async def main() -> None:
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.include_router(router)
    register_lifecycle(dp, bot)

    await dp.start_polling(bot)