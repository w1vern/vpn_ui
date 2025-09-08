
from typing import Protocol

from .i18n import I18nMessage, MessageKey
from .models import Button


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
    to_settings_menu = Button(
        I18nMessage(MessageKey.to_settings_menu), "to_settings_menu")
    to_main_menu = Button(
        I18nMessage(MessageKey.to_main_menu), "to_main_menu")
    to_inbounds_menu = Button(
        I18nMessage(MessageKey.to_inbounds_menu), "to_inbounds_menu")
    to_tickets_menu = Button(
        I18nMessage(MessageKey.to_tickets_menu), "to_tickets_menu")
    to_transactions_menu = Button(
        I18nMessage(MessageKey.to_transactions_menu), "to_transactions_menu")
    hide_notifications = Button(
        I18nMessage(MessageKey.hide_notifications), "hide_notifications")
    read_notifications = Button(
        I18nMessage(MessageKey.read_notifications), "read_notifications")


def main_menu_keyboard() -> list[Button]:
    values: list[Button] = []
    values.append(StaticButtons.to_inbounds_menu)
    values.append(StaticButtons.to_transactions_menu)
    values.append(StaticButtons.to_inbounds_menu)
    return values


def inbounds_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]


def transactions_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]


def settings_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]


def tickets_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]
