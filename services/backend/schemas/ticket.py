

from uuid import UUID
from pydantic import BaseModel
from shared.database import Ticket


class NewTicketSchema(BaseModel):
    title: str

class TicketMessageSchema(BaseModel):
    message: str

class TicketSchema(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    opening_data: str
    is_open: bool

    @classmethod
    def from_db(cls, ticket: Ticket) -> 'TicketSchema':
        return cls(
            id=ticket.id,
            user_id=ticket.holder_id,
            title=ticket.title,
            opening_data=ticket.opening_date.isoformat(),
            is_open=ticket.is_open
        )
    