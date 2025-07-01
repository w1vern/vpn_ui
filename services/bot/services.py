
from aiogram import types
from fast_depends import Depends
from redis.asyncio import Redis

from .depends import Handler, get_state
from .keyboards import (
    StaticButtons,
    main_menu_keyboard,
    settings_keyboard
)
from .redis import get_redis_client
from .states import AppStates, MyState


async def to_main_menu(message: types.Message,
                       state: MyState = Depends(get_state)
                       ) -> None:
    await state.set_state(AppStates.main_menu)
    await message.answer(text="use keyboard", reply_markup=main_menu_keyboard())


async def need_more_buttons_note(message: types.Message,
                                 state: MyState = Depends(get_state)
                                 ) -> None:
    await message.answer(text="chose another button")


async def edit_settings(message: types.Message,
                        redis: Redis = Depends(get_redis_client)
                        ) -> None:
    await state.set_state(AppStates.settings_menu)
    await message.answer(text="use keyboard", reply_markup=settings_keyboard())


async def incorrect_input(message: types.Message,
                          state: MyState = Depends(get_state)
                          ) -> None:
    await message.answer(text="error, use keyboard")


def get_func(current_state: str | None,
             message: str | None
             ) -> Handler:
    if not current_state:
        raise Exception("current state is None")
    if not message:
        raise Exception("message is None")
    func = behavioral_dict.get(f"{current_state}/{message}")
    if not func:
        func = behavioral_dict.get(current_state)
    if not func:
        func = incorrect_input
    return func


behavioral_dict: dict[str, Handler] = {
    f"{AppStates.main_menu.to_str}/{StaticButtons.to_settings_menu.text}": edit_settings,
    f"{AppStates.settings_menu.to_str}": incorrect_input,
    f"{AppStates.settings_menu.to_str}/{StaticButtons.todo_note.text}": need_more_buttons_note,
    f"{AppStates.settings_menu.to_str}/{StaticButtons.to_main_menu.text}": to_main_menu
}
