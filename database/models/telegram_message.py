import uuid
from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base
from database.models.user import User


class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    text: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    recipient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    sender: Mapped[User] = relationship(
        foreign_keys=[sender_id], lazy="selectin")
    recipient: Mapped[User] = relationship(
        foreign_keys=[recipient_id], lazy="selectin")
