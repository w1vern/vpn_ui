
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    MessageForTicketRepository,
    MessageTicketType,
    Ticket,
    TicketRepository,
    UserRepository
)

from ..depends import (
    get_message_repo,
    get_session,
    get_ticket_repo,
    get_user,
    get_user_repo
)
from ..exceptions import TicketNotFoundException
from ..schemas import (
    TicketMessageCreateSchema,
    TicketMessageSchema,
    TicketSchema,
    UserSchema
)


class TicketService:
    def __init__(
        self,
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
    def depends(
        cls,
        session: AsyncSession = Depends(get_session),
        tr: TicketRepository = Depends(get_ticket_repo),
        ur: UserRepository = Depends(get_user_repo),
        mr: MessageForTicketRepository = Depends(get_message_repo),
        user_schema: UserSchema = Depends(get_user)
    ) -> 'TicketService':
        return cls(session, tr, ur, mr, user_schema)

    async def get_ticket(
        self,
        ticket_id: UUID
    ) -> Ticket:
        ticket = await self.tr.get_by_id(ticket_id)
        if ticket is None:
            raise TicketNotFoundException()
        return ticket

    async def all(self) -> list[TicketSchema]:
        return [TicketSchema.from_db(t) for t in await self.tr.get_all()]

    async def get(
        self,
        ticket_id: UUID
    ) -> TicketSchema:
        ticket = await self.get_ticket(ticket_id)
        result = TicketSchema.from_db(ticket)
        result.messages = [TicketMessageSchema.from_db(m)
                           for m in await self.mr.get_all_by_ticket(ticket)]
        return result

    async def new_message(
        self,
        ticket_id: UUID,
        message: TicketMessageCreateSchema
    ) -> TicketMessageSchema:
        ticket = await self.get_ticket(ticket_id)
        message_db = await self.mr.create(
            text=message.message,
            ticket=ticket,
            message_type=MessageTicketType.from_admin.value
        )
        return TicketMessageSchema.from_db(message_db)

    async def close(
        self,
        ticket_id: UUID
    ) -> TicketSchema:
        ticket = await self.get_ticket(ticket_id)
        await self.tr.close(ticket)
        return TicketSchema.from_db(ticket)
