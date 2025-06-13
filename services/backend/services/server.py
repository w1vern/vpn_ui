
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import ServerRepository, UserRepository

from ..schemas import UserSchema
from .depends import get_server_repo, get_session, get_user, get_user_repo


class ServerService:
    def __init__(self,
                 session: AsyncSession,
                 ur: UserRepository,
                 sr: ServerRepository,
                 user_schema: UserSchema
                 ) -> None:
        self.session = session
        self.ur = ur
        self.sr = sr

    @classmethod
    def depends(cls,
                session: AsyncSession = Depends(get_session),
                ur: UserRepository = Depends(get_user_repo),
                sr: ServerRepository = Depends(get_server_repo),
                user_schema: UserSchema = Depends(get_user)
                ) -> 'ServerService':
        return cls(session, ur, sr, user_schema)
