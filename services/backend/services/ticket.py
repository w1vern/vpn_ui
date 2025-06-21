
from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import TicketNotFoundException
from shared.database import (
    TicketRepository,
    UserRepository,
    MessageForTicketRepository,
    Ticket,
    MessageTicketType,
)

from ..schemas import (
    UserSchema,
    TicketSchema,
    TicketMessageSchema,
    TicketMessageCreateSchema,
)

from .depends import (
    get_session,
    get_ticket_repo,
    get_user,
    get_db_user,
    get_user_repo,
    get_message_repo
)


class TicketService:
    def __init__(self,
                 session: AsyncSession,
                 tr: TicketRepository,
                 ur: UserRepository,
                 mr: MessageForTicketRepository,
                 user_schema: UserSchema
                 ) -> None:
        self.session = session
        self.tr = tr
        self.ur = ur
        self.mr = mr
        self.user_schema = user_schema

    @classmethod
    def depends(cls,
                session: AsyncSession = Depends(get_session),
                tr: TicketRepository = Depends(get_ticket_repo),
                ur: UserRepository = Depends(get_user_repo),
                mr: MessageForTicketRepository = Depends(get_message_repo),
                user_schema: UserSchema = Depends(get_user)
                ) -> 'TicketService':
        return cls(session, tr, ur, mr, user_schema)

    @staticmethod
    async def get_ticket(ticket_id: UUID,
                         tr: TicketRepository = Depends(get_ticket_repo)
                         ) -> Ticket:
        ticket = await tr.get_by_id(ticket_id)
        if ticket is None:
            raise TicketNotFoundException()
        return ticket

    async def all(self) -> list[TicketSchema]:
        return [TicketSchema.from_db(t) for t in await self.tr.get_all()]

    async def get(self,
                  ticket_id: UUID
                  ) -> TicketSchema:
        ticket = await self.get_ticket(ticket_id)
        result = TicketSchema.from_db(ticket)
        result.messages = [TicketMessageSchema.from_db(m)
                           for m in await self.mr.get_all_by_ticket(ticket)]
        return result

    async def new_message(self,
                          ticket_id: UUID,
                          message: TicketMessageCreateSchema
                          ) -> None:
        ticket = await self.get_ticket(ticket_id)
        await self.mr.create(message.message, ticket, MessageTicketType.from_admin.value)

    async def close(self,
                    ticket_id: UUID
                    ) -> None:
        ticket = await self.get_ticket(ticket_id)
        await self.tr.close(ticket)
