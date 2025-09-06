
from enum import Enum


class MessageKey(str, Enum):

    to_main_menu = "to_main_menu"
    to_settings_menu = "to_settings_menu"
    to_inbounds_menu = "to_inbounds_menu"
    to_tickets_menu = "to_tickets_menu"
    to_transactions_menu = "to_transactions_menu"
    hide_notifications = "hide_notifications"
    read_notifications = "read_notifications"

    message_user_is_none_exception = "message_user_is_none_exception"
    message_username_is_none_exception = "message_username_is_none_exception"
    send_feedback_to_admin_exception = "send_feedback_to_admin_exception"
    user_not_found_exception = "user_not_found_exception"
    incorrect_state_exception = "incorrect_state_exception"
    message_text_is_none_exception = "message_text_is_none_exception"

    telegram_api_error = "telegram_api_error"
    unknown_error = "unknown_error"

    bot_started = "bot_started"
    bot_stopped = "bot_stopped"

    welcome_message = "welcome_message"
    dont_use_start_command = "dont_use_start_command"

    settings_menu = "settings_menu"
    inbounds_menu = "inbounds_menu"
    tickets_menu = "tickets_menu"
    transactions_menu = "transactions_menu"
    main_menu = "main_menu"

    balance = "balance"
