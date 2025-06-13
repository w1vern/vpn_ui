
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import TicketRepository

from ..schemas import UserSchema
from .depends import get_session, get_ticket_repo, get_user


class TicketService:
    def __init__(self,
                 session: AsyncSession,
                 tr: TicketRepository,
                 user_schema: UserSchema
                 ) -> None:
        self.session = session
        self.tr = tr
        self.user_schema = user_schema

    @classmethod
    def depends(cls,
                session: AsyncSession = Depends(get_session),
                tr: TicketRepository = Depends(get_ticket_repo),
                user_schema: UserSchema = Depends(get_user)
                ) -> 'TicketService':
        return cls(session, tr, user_schema)
