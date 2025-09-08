

import json

from shared.database import LanguageCodes
from shared.infrastructure import setup_logger

from .i18n import I18nMessage, MessageKey

logger = setup_logger(__name__)


class UserInfo:
    def __init__(self, id: int,
                 username: str,
                 lang_code: LanguageCodes
                 ) -> None:
        self.id = id
        self.username = username
        self.lang_code = lang_code


class Notification():
    def __init__(self,
                 text: str
                 ) -> None:
        self.text = text


class Button():
    def __init__(self,
                 text: I18nMessage,
                 callback_data: str,
                 for_member: bool = True,
                 for_admin: bool = False
                 ) -> None:
        self.text = text
        self.callback_data = callback_data
        self.for_member = for_member
        self.for_admin = for_admin


class Output:
    def __init__(self,
                 text: str | None,
                 buttons: list[Button] | None,
                 user_info: UserInfo,
                 notify: bool = False
                 ) -> None:
        self.text = text
        self.buttons = buttons
        self.user_info = user_info
        self.notify = notify


class MainMessage():
    def __init__(self,
                 text: list[str],
                 notifications: list[Notification],
                 buttons: list[Button]
                 ) -> None:
        self.text = text
        self.notifications = notifications
        self.buttons = buttons

    def to_str(self) -> str:
        return json.dumps({
            "text": self.text,
            "notifications": [{"text": notification.text} for notification in self.notifications],
            "buttons": [{
                "text": button.text.message_key.value,
                "callback_data": button.callback_data,
                "for_member": button.for_member,
                "for_admin": button.for_admin
            } for button in self.buttons]
        })

    @classmethod
    def from_str(cls, s: str) -> "MainMessage":
        data = json.loads(s)
        logger.debug(data)
        return cls(data["text"],
                   [Notification(notification["text"])
                    for notification in data["notifications"]],
                   [Button(I18nMessage(MessageKey(button["text"])),
                           button["callback_data"],
                           button["for_member"],
                           button["for_admin"]
                           ) for button in data["buttons"]])
