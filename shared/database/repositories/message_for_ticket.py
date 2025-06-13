

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from ..models import (
    MessageForTicket,
    Ticket,
)
from .base import (
    BaseRepository,
)


class MessageForTicketRepository(BaseRepository[MessageForTicket]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MessageForTicket)

    async def create(self,
                     text: str,
                     ticket: Ticket,
                     message_type: str
                     ) -> MessageForTicket:
        return await self.universal_create(
            text=text,
            ticket_id=ticket.id,
            message_type=message_type)

    async def get_all_by_ticket(self,
                                ticket: Ticket
                                ) -> list[MessageForTicket]:
        stmt = select(MessageForTicket).where(
            MessageForTicket.ticket_id == ticket.id)
        return list((await self.session.scalars(stmt)).all())
