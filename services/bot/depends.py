

from uuid import UUID
from .exceptions import (
    MessageUserIsNoneException,
    MessageUsernameIsNoneException,
    UserNotFoundException
)
from shared.database import (
    UserRepository,
    User,
    session_manager,
)

from aiogram.types import Message
from fast_depends import Depends
from sqlalchemy.ext.asyncio import AsyncSession


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
