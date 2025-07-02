
from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InaccessibleMessage,
    Message,
    InlineKeyboardMarkup
)
from fast_depends import Depends, inject
from redis.asyncio import Redis

from .exceptions import MessageTextIsNoneException
from .keyboard import create_keyboard
from .redis import RedisType, get_redis_client
from .services import Output, Service
from .bot import get_bot

router = Router()


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
async def update_inline(new_state: Output,
                        redis: Redis = Depends(get_redis_client)
                        ) -> None:
    message_id = await redis.get(f"{RedisType.main_message}:{new_state.user_info.id}")
    chat_id = new_state.user_info.id
    await edit_message(get_bot(),
                       chat_id,
                       message_id,
                       new_state.text,
                       create_keyboard(new_state.buttons)
                       if new_state.buttons is not None else None)


@router.message(Command("start"))
@inject
async def cmd_start(message: Message,
                    service: Service = Depends(Service.depends)
                    ) -> None:
    await message.delete()
    await update_inline(await service.start_handler())


@router.message()
@inject
async def handle_text(message: Message,
                      service: Service = Depends(Service.depends)
                      ) -> None:
    await message.delete()
    if message.text is None:
        raise MessageTextIsNoneException()
    await update_inline(await service.chat_handler(message.text))


@router.callback_query()
@inject
async def handle_inline_button(callback_query: CallbackQuery,
                               service: Service = Depends(Service.depends)
                               ) -> None:
    if callback_query.message is None \
        or isinstance(callback_query.message, InaccessibleMessage) \
            or callback_query.message.text is None:
        raise MessageTextIsNoneException()
    await update_inline(await service.keyboard_handler(callback_query.message.text))
