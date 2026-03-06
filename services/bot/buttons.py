
from typing import Protocol

from .i18n import I18nMessage, MessageKey
from .models import Button


class GetKeyboardSizeFunction(Protocol):
    def __call__(self,
                 values: list[Button]
                 ) -> list[int]:
        ...


def get_keyboard_size(
    values: list[Button]
) -> list[int]:
    in_a_row = 2
    length = len(values)
    res: list[int] = []
    for _ in range(in_a_row, length + 1, in_a_row):
        res.append(in_a_row)
    if length % in_a_row:
        res.append(length % in_a_row)
    return res


class StaticButtons:
    to_settings_menu = Button(
        I18nMessage(MessageKey.to_settings_menu),
        "to_settings_menu"
    )
    to_main_menu = Button(
        I18nMessage(MessageKey.to_main_menu),
        "to_main_menu"
    )
    to_inbounds_menu = Button(
        I18nMessage(MessageKey.to_inbounds_menu),
        "to_inbounds_menu"
    )
    to_tickets_menu = Button(
        I18nMessage(MessageKey.to_tickets_menu),
        "to_tickets_menu"
    )
    to_transactions_menu = Button(
        I18nMessage(MessageKey.to_transactions_menu),
        "to_transactions_menu"
    )
    read_notifications = Button(
        I18nMessage(MessageKey.read_notifications),
        "read_notifications"
    )
    to_tariffs_menu = Button(
        I18nMessage(MessageKey.to_tariffs_menu),
        "to_tariffs_menu"
    )
    reset_key = Button(
        I18nMessage(MessageKey.reset_key),
        "reset_key"
    )
    switch_language = Button(
        I18nMessage(MessageKey.switch_language),
        "switch_language"
    )
    toggle_auto_pay = Button(
        I18nMessage(MessageKey.toggle_auto_pay),
        "toggle_auto_pay"
    )
    toggle_get_traffic_notifications = Button(
        I18nMessage(MessageKey.toggle_get_traffic_notifications),
        "toggle_get_traffic_notifications"
    )


def main_menu_keyboard() -> list[Button]:
    values: list[Button] = []
    values.append(StaticButtons.to_inbounds_menu)
    values.append(StaticButtons.to_transactions_menu)
    #values.append(StaticButtons.to_settings_menu)
    #values.append(StaticButtons.to_tariffs_menu)
    return values


def inbounds_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]


def transactions_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]


def settings_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]


def tariffs_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]


def tickets_keyboard() -> list[Button]:
    return [StaticButtons.to_main_menu]
