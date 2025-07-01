
from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.types import InlineKeyboardMarkup

from shared.config import env_config

from .handlers import router
from .lifecycle import register_lifecycle


async def edit_message(chat_id: int,
                       message_id: int,
                       new_text: str | None,
                       new_keyboard: InlineKeyboardMarkup | None
                       ) -> None:
    if not new_text is None:
        await bot.edit_message_text(new_text,
                                    chat_id=chat_id,
                                    message_id=message_id)
    if not new_keyboard is None:
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=new_keyboard)

bot = Bot(token=env_config.bot.token)
dp = Dispatcher()
dp.include_router(router)

register_lifecycle(dp, bot)


def get_bot() -> Bot:
    return bot
