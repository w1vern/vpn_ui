
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User


class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    text: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    sender_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    recipient_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    sender: Mapped[User] = relationship(
        foreign_keys=[sender_id], lazy="selectin")
    recipient: Mapped[User] = relationship(
        foreign_keys=[recipient_id], lazy="selectin")
