
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import TicketRepository, UserRepository

from ..schemas import (
    UserSchema,
    TicketSchema,
    TicketMessageSchema,
    NewTicketSchema
)
from .depends import (
    get_session,
    get_ticket_repo,
    get_user,
    get_db_user,
    get_user_repo
)


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
                ur: UserRepository = Depends(get_user_repo),
                user_schema: UserSchema = Depends(get_user)
                ) -> 'TicketService':
        return cls(session, tr, user_schema)

    async def all(self) -> list[TicketSchema]:
        return [TicketSchema.from_db(t) for t in await self.tr.get_all()]

    async def create(self,
                     new_ticket: NewTicketSchema
                     ) -> None:
        pass