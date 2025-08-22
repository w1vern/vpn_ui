

import json

from shared.infrastructure import setup_logger

logger = setup_logger(__name__)


class UserInfo:
    def __init__(self, id: int,
                 username: str
                 ) -> None:
        self.id = id
        self.username = username


class Notification():
    def __init__(self,
                 text: str
                 ) -> None:
        self.text = text


class Button():
    def __init__(self,
                 text: str,
                 for_member: bool = True,
                 ) -> None:
        self.text = text
        self.for_member = for_member


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
                 text: str,
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
                "text": button.text,
                "for_member": button.for_member
            } for button in self.buttons]
        })

    @classmethod
    def from_str(cls, s: str) -> "MainMessage":
        data = json.loads(s)
        logger.debug(data)
        return cls(data["text"],
                   [Notification(notification["text"])
                    for notification in data["notifications"]],
                   [Button(button["text"], button["for_member"]) for button in data["buttons"]])
