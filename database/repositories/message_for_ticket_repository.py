from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.enums import *
from database.models import *


class MessageForTicketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, text: str, ticket: Ticket, type: MessageTicketType) -> None:
        self.session.add(MessageForTicket(text=text, ticket_id=ticket.id, type=type))
        await self.session.flush()

    async def get_message_by_ticket(self, ticket: Ticket) -> list[MessageForTicket]:
        stmt = select(MessageForTicket).where(MessageForTicket.ticket_id == ticket.id)
        return list((await self.session.scalars(stmt)).all())