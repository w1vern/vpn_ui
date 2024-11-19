
from datetime import UTC, datetime

import redis
from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from back.token import AccessToken
from database.database import get_db_session
from database.models.user import User
from database.repositories.user_repository import UserRepository


async def get_user(access_token: str = Cookie(default=None), session: AsyncSession = Depends(get_db_session)) -> User:
    if access_token is None:
        raise HTTPException(status_code=401, detail="access token doesn't exist")
    access = AccessToken.from_token(access_token)
    current_time = datetime.now(UTC)
    if access.created_date > current_time or access.created_date + access.lifetime < current_time:
        raise HTTPException(status_code=401, detail="access token expired")
    user_id = access.user_id
    if user_id is None:
        raise HTTPException(status_code=401, detail="access token damaged")
    ur = UserRepository(session)
    user = await ur.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    return user