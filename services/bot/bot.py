
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError
from aiogram.types import InlineKeyboardMarkup
from fast_depends import Depends, inject
from redis.asyncio import Redis

from shared.infrastructure import env_config, setup_logger

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
                                    message_id=message_id,
                                    # parse_mode="MarkdownV2"
                                    )
    if not new_keyboard is None:
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=new_keyboard)


async def send_message(bot: Bot,
                       redis: Redis,
                       chat_id: int,
                       text: str,
                       keyboard: InlineKeyboardMarkup
                       ) -> None:
    message = await bot.send_message(chat_id=chat_id,
                                     text=text,
                                     reply_markup=keyboard,
                                     # parse_mode="MarkdownV2"
                                     )
    await redis.set(f"{RedisType.main_message_id.value}:{chat_id}", message.message_id)
    logger.debug(f"message_id: {message.message_id}")


@inject
async def update_message(new_state: Output,
                         redis: Redis = Depends(get_redis_client),
                         bot: Bot = Depends(get_bot)
                         ) -> None:
    # if new_state.text is not None:
    #    new_state.text.replace(".", "\\.")
    message_id: int | None = await redis.get(f"{RedisType.main_message_id.value}:{new_state.user_info.id}")
    logger.debug(f"message_id: {message_id}")
    if not message_id is None:
        chat_id = new_state.user_info.id
        if not new_state.notify:
            await edit_message(bot,
                               chat_id,
                               message_id,
                               new_state.text,
                               create_keyboard(
                                   new_state.buttons, new_state.user_info.lang_code)
                               if new_state.buttons is not None else None)
            return
        else:
            try:
                await bot.delete_message(chat_id=new_state.user_info.id, message_id=message_id)
            except TelegramAPIError:
                ...
    if new_state.text is None or new_state.buttons is None:
        raise SendFeedbackToAdminException()
    await send_message(bot,
                       redis,
                       new_state.user_info.id,
                       new_state.text,
                       create_keyboard(new_state.buttons, new_state.user_info.lang_code))
