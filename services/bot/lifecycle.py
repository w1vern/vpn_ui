
from aiogram import Bot, Dispatcher
from fast_depends import Depends, inject
from redis.asyncio import Redis

from shared.database import UserRepository

from .buttons import main_menu_keyboard
from .depends import get_user_repo
from .keyboard import create_keyboard
from .redis import RedisType, get_redis_client
from .states import AppStates


def register_lifecycle(dp: Dispatcher,
                       bot: Bot
                       ) -> None:
    @dp.startup()
    @inject
    async def on_startup(ur: UserRepository = Depends(get_user_repo),
                         redis: Redis = Depends(get_redis_client)
                         ) -> None:
        users = await ur.get_all()
        for user in users:
            prev_message = await redis.get(f"{RedisType.main_message}:{user.telegram_id}")
            if prev_message is not None:
                await bot.delete_message(chat_id=user.telegram_id, message_id=prev_message)
            message = await bot.send_message(
                chat_id=user.telegram_id,
                text="bot startup",
                reply_markup=create_keyboard(main_menu_keyboard()))
            await redis.set(f"{RedisType.main_message}:{user.telegram_id}", message.message_id)
            await redis.set(f"{RedisType.state}:{user.telegram_id}", AppStates.main_menu.to_str)

    @dp.shutdown()
    @inject
    async def on_shutdown(ur: UserRepository = Depends(get_user_repo),
                          redis: Redis = Depends(get_redis_client)
                          ) -> None:
        users = await ur.get_all()
        for user in users:
            message_id = await redis.get(f"{RedisType.main_message}:{user.telegram_id}")
            await bot.edit_message_text(
                chat_id=user.telegram_id,
                message_id=message_id,
                text="bot shutdown",
                reply_markup=None)
