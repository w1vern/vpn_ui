
import json
from uuid import UUID

from aiogram.types import CallbackQuery, Message
from fast_depends import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import User, UserRepository, session_manager

from .buttons import Button
from .exceptions import (
    MessageUserIsNoneException,
    MessageUsernameIsNoneException,
    SendFeedbackToAdminException,
    UserNotFoundException
)
from .redis import RedisType, get_redis_client
from .states import MyState


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


class MainMessage():
    def __init__(self,
                 id: int,
                 text: str,
                 notifications: list[Notification],
                 buttons: list[Button]
                 ) -> None:
        self.id = id
        self.text = text
        self.notifications = notifications
        self.buttons = buttons

    def to_str(self) -> str:
        return json.dumps({
            "id": self.id,
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
        return cls(data["id"],
                   data["text"],
                   [Notification(notification["text"]) for notification in data["notifications"]],
                   [Button(button["text"], button["for_member"]) for button in data["buttons"]])


async def get_user_repo(session: AsyncSession = Depends(session_manager.session)
                        ) -> UserRepository:
    return UserRepository(session)


async def get_user_info(message: Message | None = None,
                        callback_query: CallbackQuery | None = None
                        ) -> UserInfo:
    if message is None:
        if not callback_query is None:
            data = callback_query
        else:
            raise SendFeedbackToAdminException()
    else:
        data = message
    if not data.from_user:
        raise MessageUserIsNoneException()
    if not data.from_user.username:
        raise MessageUsernameIsNoneException()
    return UserInfo(data.from_user.id,
                    data.from_user.username)

async def get_request_data(message: Message | None = None,
                   callback_query: CallbackQuery | None = None
                   ) -> str:
    if message is None:
        if not callback_query is None:
            data = callback_query.data
        else:
            raise SendFeedbackToAdminException()
    else:
        data = message.text
    if data is None:
        raise SendFeedbackToAdminException()
    return data
    


async def create_user(user_info: UserInfo = Depends(get_user_info),
                      ur: UserRepository = Depends(get_user_repo)
                      ) -> User:

    user = await ur.get_by_telegram_id(user_info.id)
    if user:
        return user
    user = await ur.create(user_info.id,
                           user_info.username,
                           UUID(int=0))
    return user


async def get_user(user_info: UserInfo = Depends(get_user_info),
                   ur: UserRepository = Depends(get_user_repo)
                   ) -> User:
    user = await ur.get_by_telegram_id(user_info.id)
    if user:
        if user.telegram_username != user_info.username:
            await ur.update_telegram_username(user, user_info.username)
        return user
    raise UserNotFoundException()


async def get_state(user_info: UserInfo = Depends(get_user_info),
                    redis: Redis = Depends(get_redis_client)
                    ) -> MyState:
    state = await redis.get(f"{RedisType.state.value}:{user_info.id}")
    return MyState.from_str(state)


async def get_main_message(user_info: UserInfo = Depends(get_user_info),
                           redis: Redis = Depends(get_redis_client)
                           ) -> MainMessage:
    return MainMessage.from_str(await redis.get(f"{RedisType.main_message.value}:{user_info.id}"))
