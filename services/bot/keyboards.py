
from typing import Protocol

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class StaticButton():
    def __init__(self,
                 text: str,
                 only_for_admin: bool = False,
                 ) -> None:
        self.text = text
        self.only_for_admin = only_for_admin


class GetKeyboardSizeFunction(Protocol):
    def __call__(self,
                 values: list[str]
                 ) -> list[int]:
        ...


def get_keyboard_size(values: list[str]
                      ) -> list[int]:
    in_a_row = 4
    length = len(values)
    res: list[int] = []
    for _ in range(in_a_row, length + 1, in_a_row):
        res.append(4)
    if length % in_a_row:
        res.append(length % in_a_row)
    return res


def create_keyboard(values: list[str],
                    placeholder: str = "",
                    keyboard_size: GetKeyboardSizeFunction = get_keyboard_size
                    ) -> ReplyKeyboardMarkup:
    markup = keyboard_size(values)
    keyboard: list[list[KeyboardButton]] = []
    index = 0
    for i in range(len(markup)):
        keyboard.append([])
        for _ in range(markup[i]):
            keyboard[i].append(KeyboardButton(text=values[index]))
            index += 1

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )


class StaticButtons:
    to_settings_menu = StaticButton("settings")
    to_main_menu = StaticButton("back to main menu")
    to_inbounds_menu = StaticButton("inbounds menu")
    to_tickets_menu = StaticButton("tickets menu")
    todo_note = StaticButton("need more buttons there")


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    values: list[str] = []
    values.append(StaticButtons.to_settings_menu.text)
    values.append(StaticButtons.to_inbounds_menu.text)
    values.append(StaticButtons.to_tickets_menu.text)
    return create_keyboard(values)


def settings_keyboard() -> ReplyKeyboardMarkup:
    return create_keyboard([StaticButtons.todo_note.text, StaticButtons.to_main_menu.text])


def inbounds_keyboard() -> ReplyKeyboardMarkup:
    return create_keyboard([StaticButtons.todo_note.text, StaticButtons.to_main_menu.text])


def tickets_keyboard() -> ReplyKeyboardMarkup:
    return create_keyboard([StaticButtons.todo_note.text, StaticButtons.to_main_menu.text])
