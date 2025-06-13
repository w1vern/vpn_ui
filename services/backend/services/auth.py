
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import UserRepository

from .depends import get_session, get_user_repo


class AuthService:
    def __init__(self,
                 session: AsyncSession,
                 ur: UserRepository,
                 ) -> None:
        self.session = session
        self.ur = ur

    @classmethod
    def depends(cls,
                session: AsyncSession = Depends(get_session),
                ur: UserRepository = Depends(get_user_repo),
                ) -> 'AuthService':
        return cls(session, ur)
