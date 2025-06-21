

from uuid import UUID

from pydantic import BaseModel

from shared.database import MessageForTicket, Ticket


class NewTicketSchema(BaseModel):
    title: str


class TicketMessageCreateSchema(BaseModel):
    message: str


class TicketMessageSchema(BaseModel):
    id: UUID
    message: str
    date: str

    @classmethod
    def from_db(cls, message: MessageForTicket) -> 'TicketMessageSchema':
        return cls(
            id=message.id,
            message=message.text,
            date=message.date.isoformat()
        )


class TicketSchema(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    opening_data: str
    is_open: bool
    messages: list[TicketMessageSchema] | None = None

    @classmethod
    def from_db(cls, ticket: Ticket) -> 'TicketSchema':
        return cls(
            id=ticket.id,
            user_id=ticket.holder_id,
            title=ticket.title,
            opening_data=ticket.opening_date.isoformat(),
            is_open=ticket.is_open
        )
