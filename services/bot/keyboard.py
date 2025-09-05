
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .buttons import (
    Button,
    GetKeyboardSizeFunction,
    get_keyboard_size
)
from .i18n import LanguageCodes


def create_keyboard(values: list[Button],
                    lang_code: LanguageCodes,
                    keyboard_size: GetKeyboardSizeFunction = get_keyboard_size,
                    ) -> InlineKeyboardMarkup:
    markup = keyboard_size(values)
    keyboard: list[list[InlineKeyboardButton]] = []
    index = 0
    for i in range(len(markup)):
        keyboard.append([])
        for _ in range(markup[i]):
            keyboard[i].append(InlineKeyboardButton(text=values[index].text.render(lang_code),
                                                    callback_data=values[index].callback_data))
            index += 1

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
