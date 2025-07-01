
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .buttons import (
    Button,
    GetKeyboardSizeFunction,
    get_keyboard_size
)


def create_keyboard(values: list[Button],
                    keyboard_size: GetKeyboardSizeFunction = get_keyboard_size
                    ) -> InlineKeyboardMarkup:
    markup = keyboard_size(values)
    keyboard: list[list[InlineKeyboardButton]] = []
    index = 0
    for i in range(len(markup)):
        keyboard.append([])
        for _ in range(markup[i]):
            keyboard[i].append(InlineKeyboardButton(text=values[index].text,
                                                    callback_data=values[index].text))
            index += 1

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
