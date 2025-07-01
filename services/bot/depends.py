
from typing import Awaitable, Protocol
from uuid import UUID

from aiogram.types import Message
from fast_depends import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    User,
    UserRepository,
    session_manager,
)

from .exceptions import (
    MessageUserIsNoneException,
    MessageUsernameIsNoneException,
    UserNotFoundException
)
from .redis import RedisType, get_redis_client
from .states import MyState


class Handler(Protocol):
    def __call__(self,
                 message: Message,
                 ) -> Awaitable[None]:
        ...


class UserInfo:
    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username


async def get_user_repo(session: AsyncSession = Depends(session_manager.session)
                        ) -> UserRepository:
    return UserRepository(session)


async def get_user_info(message: Message) -> UserInfo:
    if not message.from_user:
        raise MessageUserIsNoneException()
    if not message.from_user.username:
        raise MessageUsernameIsNoneException()
    return UserInfo(message.from_user.id,
                    message.from_user.username)


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
    state = await redis.get(f"{RedisType.state}:{user_info.id}")
    return MyState.from_str(state)
