from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey, func
from app.database.database import Base
from uuid import uuid4

from datetime import datetime

from app.database.models.user import User
from app.database.models.ticket import Ticket
from app.database.enums.ticket_message_type import MessageTicketType

class MessageForTicket(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    text: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column(default=func.now())
    from_user: Mapped[MessageTicketType] = mapped_column()
    ticket_id: Mapped[UUID] = mapped_column(ForeignKey("tickets.id"))
    
    ticket: Mapped[Ticket] = relationship(lazy="selectin")

