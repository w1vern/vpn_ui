
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import ReplyKeyboardRemove
from fast_depends import Depends, inject

from shared.database import UserRepository

from .config import env_config
from .depends import get_user_repo

# from .keyboards import main_menu_keyboard
from .states import AppState


def register_lifecycle(dp: Dispatcher, bot: Bot) -> None:
    @dp.startup()
    @inject
    async def on_startup(ur: UserRepository = Depends(get_user_repo)
                         ) -> None:
        users = await ur.get_all()
        for user in users:
            state = FSMContext(storage=dp.storage, key=StorageKey(
                bot.id, user.telegram_id, user.telegram_id))
            await state.set_state(AppState.main_menu)
            # await bot.send_message(chat_id=user.telegram_id, text="bot startup", reply_markup=main_menu_keyboard(user))

    @dp.shutdown()
    @inject
    async def on_shutdown(ur: UserRepository = Depends(get_user_repo)
                          ) -> None:
        for user in await ur.get_all():
            pass
        await bot.send_message(env_config.bot.superuser,
                               "bot shuting down",
                               reply_markup=ReplyKeyboardRemove())
