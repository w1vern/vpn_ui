
from typing import Protocol


class Button():
    def __init__(self,
                 text: str,
                 for_member: bool = True,
                 ) -> None:
        self.text = text
        self.for_member = for_member


class GetKeyboardSizeFunction(Protocol):
    def __call__(self,
                 values: list[Button]
                 ) -> list[int]:
        ...


def get_keyboard_size(values: list[Button]
                      ) -> list[int]:
    in_a_row = 4
    length = len(values)
    res: list[int] = []
    for _ in range(in_a_row, length + 1, in_a_row):
        res.append(4)
    if length % in_a_row:
        res.append(length % in_a_row)
    return res


class StaticButtons:
    to_settings_menu = Button("settings")
    to_main_menu = Button("back to main menu")
    to_inbounds_menu = Button("inbounds menu")
    to_tickets_menu = Button("tickets menu")
    to_transactions_menu = Button("transactions menu")
    hide_notifications = Button("hide notifications")


def main_menu_keyboard() -> list[Button]:
    values: list[Button] = []
    values.append(StaticButtons.to_inbounds_menu)
    values.append(StaticButtons.to_transactions_menu)
    return values


def inbounds_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]


def transactions_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]


def settings_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]


def tickets_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]
