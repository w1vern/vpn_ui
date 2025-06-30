
from aiogram import types
from aiogram.fsm.context import FSMContext
from bot.states import AppState

from .depends import Handler
from .keyboards import (
    StaticButtons,
    main_menu_keyboard,
    settings_keyboard
)


async def to_main_menu(message: types.Message,
                       state: FSMContext,
                       ) -> None:
    await state.set_state(AppState.main_menu)
    await message.answer(text="use keyboard", reply_markup=main_menu_keyboard())


async def need_more_buttons_note(message: types.Message,
                                 state: FSMContext,
                                 ) -> None:
    await message.answer(text="chose another button")


async def edit_settings(message: types.Message,
                        state: FSMContext,
                        ) -> None:
    await state.set_state(AppState.settings_menu)
    await message.answer(text="use keyboard", reply_markup=settings_keyboard())


async def incorrect_input(message: types.Message,
                          state: FSMContext,
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
    f"{AppState.main_menu.state}/{StaticButtons.to_settings_menu.text}": edit_settings,
    f"{AppState.settings_menu.state}": incorrect_input,
    f"{AppState.settings_menu.state}/{StaticButtons.todo_note.text}": need_more_buttons_note,
    f"{AppState.settings_menu.state}/{StaticButtons.to_main_menu.text}": to_main_menu
}
