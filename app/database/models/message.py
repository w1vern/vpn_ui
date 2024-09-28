from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey
from app.database.database import Base
from uuid import uuid4

from app.database.models.user import User
from app.database.models.ticket import Ticket

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    text: Mapped[str] = mapped_column()
    ticket_id: Mapped[UUID] = mapped_column(ForeignKey("tickets.id"))
    sender_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    ticket: Mapped[Ticket] = relationship(lazy="selectin")
    sender: Mapped[User] = relationship(lazy="selectin")
