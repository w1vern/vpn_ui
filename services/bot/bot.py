
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError
from aiogram.types import InlineKeyboardMarkup
from fast_depends import Depends, inject
from redis.asyncio import Redis

from shared.config import env_config
from shared.infrastructure import setup_logger

from .exceptions import SendFeedbackToAdminException
from .keyboard import create_keyboard
from .models import Output
from .redis import RedisType, get_redis_client

bot = Bot(token=env_config.bot.token)
dp = Dispatcher()

logger = setup_logger(__name__)


def get_bot() -> Bot:
    return bot


async def edit_message(bot: Bot,
                       chat_id: int,
                       message_id: int,
                       new_text: str | None,
                       new_keyboard: InlineKeyboardMarkup | None,
                       ) -> None:
    if not new_text is None:
        await bot.edit_message_text(new_text,
                                    chat_id=chat_id,
                                    message_id=message_id)
    if not new_keyboard is None:
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=new_keyboard)


@inject
async def update_message(new_state: Output,
                         redis: Redis = Depends(get_redis_client),
                         bot: Bot = Depends(get_bot)
                         ) -> None:
    message_id = int(await redis.get(f"{RedisType.main_message_id.value}:{new_state.user_info.id}"))
    logger.debug(f"message_id: {message_id}")
    chat_id = new_state.user_info.id
    if not new_state.notify:
        await edit_message(bot,
                           chat_id,
                           message_id,
                           new_state.text,
                           create_keyboard(new_state.buttons)
                           if new_state.buttons is not None else None)
    else:
        if message_id is not None:
            try:
                await bot.delete_message(chat_id=new_state.user_info.id, message_id=message_id)
            except TelegramAPIError:
                ...
        if new_state.buttons is None or new_state.text is None:
            raise SendFeedbackToAdminException()
        message = await bot.send_message(chat_id=chat_id,
                                         text=new_state.text,
                                         reply_markup=create_keyboard(
                                             new_state.buttons)
                                         )
        await redis.set(f"{RedisType.main_message_id.value}:{new_state.user_info.id}", message.message_id)
        logger.debug(f"message_id: {message.message_id}")
