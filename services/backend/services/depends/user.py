
from datetime import (
    UTC,
    datetime,
)

from fastapi import (
    Cookie,
    Depends,
)
from redis.asyncio import Redis

from shared.database import User, UserRepository
from shared.infrastructure import (
    RedisType,
    get_redis_client,
)

from ...exceptions import (
    NotControlPanelUserException,
    SendFeedbackToAdminException,
    AccessTokenMissingException,
    AccessTokenExpiredException,
    AccessTokenInvalidatedException,
    AccessTokenCorruptedException
)
from ...schemas import UserSchema
from ...token import AccessToken


async def get_user(access_token: str | None = Cookie(default=None),
                   redis: Redis = Depends(get_redis_client)
                   ) -> UserSchema:
    if access_token is None:
        raise AccessTokenMissingException()
    access = AccessToken.from_token(access_token)
    current_time = datetime.now(UTC).replace(tzinfo=None)
    if access.created_date > current_time or access.created_date + access.lifetime < current_time:
        raise AccessTokenExpiredException()
    if await redis.exists(f"{RedisType.invalidated_access_token}:{access.user.id}"):
        raise AccessTokenInvalidatedException()
    if not access.user:
        raise AccessTokenCorruptedException()
    if access.user.rights.is_control_panel_user is False:
        raise NotControlPanelUserException()
    return access.user


async def get_db_user(user: UserSchema,
                      ur: UserRepository
                      ) -> User:
    user_db = await ur.get_by_id(user.id)
    if user_db is None:
        raise SendFeedbackToAdminException()
    return user_db
