

import uuid
from mailbox import Message
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.enums import *
from database.models import *


class MessageForTicketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, text: str, ticket: Ticket, type: int) -> Optional[MessageForTicket]:
        message_for_ticket = MessageForTicket(text=text, ticket_id=ticket.id, type=type)
        self.session.add(message_for_ticket)
        await self.session.flush()
        return await self.get_by_id(message_for_ticket.id)
    
    async def get_by_id(self, id: uuid.UUID) -> Optional[MessageForTicket]:
        stmt = select(MessageForTicket).where(MessageForTicket.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_message_by_ticket(self, ticket: Ticket) -> list[MessageForTicket]:
        stmt = select(MessageForTicket).where(MessageForTicket.ticket_id == ticket.id)
        return list((await self.session.scalars(stmt)).all())