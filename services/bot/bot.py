
from aiogram import (
    Bot,
    Dispatcher,
)

from shared.config import env_config

from .handlers import router
from .lifecycle import register_lifecycle


bot = Bot(token=env_config.bot.token)
dp = Dispatcher()
dp.include_router(router)

register_lifecycle(dp, bot)


def get_bot() -> Bot:
    return bot
