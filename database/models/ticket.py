from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey
from database.models.base import Base
from uuid import uuid4
import uuid
from datetime import datetime

from database.models.user import User


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column()
    holder_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    opening_date: Mapped[datetime] = mapped_column()
    closing_date: Mapped[datetime] = mapped_column()
    is_open: Mapped[bool] = mapped_column()

    holder: Mapped[User] = relationship(lazy="selectin")
