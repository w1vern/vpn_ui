
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import ReplyKeyboardRemove
from fast_depends import Depends, inject

from shared.database import UserRepository

from .config import env_config
from .depends import get_user_repo
from .keyboards import main_menu_keyboard
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
            message = await bot.send_message(
                chat_id=user.telegram_id,
                text="bot startup",
                reply_markup=main_menu_keyboard())
            await state.set_data({"message_id": message.message_id})

    @dp.shutdown()
    @inject
    async def on_shutdown(state: FSMContext,
                          ur: UserRepository = Depends(get_user_repo)
                          ) -> None:
        """ for user in await ur.get_all():
            pass
        chat_id  = user.telegram_id
        message_id = (await state.get_data()).get("message_id")
        await bot.delete_message() """
