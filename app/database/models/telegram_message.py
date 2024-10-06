from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey
from app.database.models.base import Base
from uuid import uuid4
import uuid
from datetime import datetime

from app.database.models.user import User


class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid4)
    text: Mapped[str] = mapped_column()
    date: Mapped[datetime]= mapped_column()
    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    recipient_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    sender: Mapped[User] = relationship(lazy="selectin")
    recipient: Mapped[User] = relationship(lazy="selectin")



