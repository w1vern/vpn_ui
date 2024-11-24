import uuid
from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.enums.message_ticket_type import MessageTicketType
from database.models.base import Base
from database.models.ticket import Ticket


class MessageForTicket(Base):
    __tablename__ = "ticket_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    text: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    type: Mapped[MessageTicketType] = mapped_column()
    ticket_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tickets.id"))
    
    ticket: Mapped[Ticket] = relationship(lazy="selectin", foreign_keys=[ticket_id])

