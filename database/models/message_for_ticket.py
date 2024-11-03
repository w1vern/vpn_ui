from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey
from app.database.models.base import Base
from uuid import uuid4
import uuid
from datetime import datetime

from app.database.models.ticket import Ticket
from app.database.enums.message_ticket_type import MessageTicketType

class MessageForTicket(Base):
    __tablename__ = "ticket_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    text: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    type: Mapped[MessageTicketType] = mapped_column()
    ticket_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tickets.id"))
    
    ticket: Mapped[Ticket] = relationship(lazy="selectin")

