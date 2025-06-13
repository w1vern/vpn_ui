
from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from .ticket import Ticket


class MessageForTicket(Base):
    __tablename__ = "ticket_messages"

    text: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    message_type: Mapped[str] = mapped_column()
    ticket_id: Mapped[UUID] = mapped_column(ForeignKey("tickets.id"))

    ticket: Mapped[Ticket] = relationship(
        lazy="selectin", foreign_keys=[ticket_id])
