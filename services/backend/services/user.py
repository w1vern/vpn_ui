
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import UserRepository

from ..schemas import UserSchema
from .depends import get_session, get_user, get_user_repo


class UserService:
    def __init__(self,
                 session: AsyncSession,
                 ur: UserRepository,
                 user_schema: UserSchema
                 ) -> None:
        self.session = session
        self.ur = ur
        self.user_schema = user_schema

    @classmethod
    def depends(cls,
                      session: AsyncSession = Depends(get_session),
                      ur: UserRepository = Depends(get_user_repo),
                      user_schema: UserSchema = Depends(get_user)
                      ) -> 'UserService':
        return cls(session, ur, user_schema)
