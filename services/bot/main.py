
from aiogram import Bot, Dispatcher

from shared.config import env_config

from .handlers import router
from .lifecycle import register_lifecycle


async def main() -> None:
    bot = Bot(token=env_config.bot.token)
    dp = Dispatcher()

    dp.include_router(router)
    register_lifecycle(dp, bot)

    await dp.start_polling(bot)