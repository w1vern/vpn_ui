
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base
from database.models.user import User


class Ticket(Base):
    __tablename__ = "tickets"

    title: Mapped[str] = mapped_column()
    holder_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    opening_date: Mapped[datetime] = mapped_column()
    closing_date: Mapped[datetime] = mapped_column()
    is_open: Mapped[bool] = mapped_column()

    holder: Mapped[User] = relationship(
        lazy="selectin", foreign_keys=[holder_id])
