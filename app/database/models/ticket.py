from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey
from app.database.database import Base
from uuid import uuid4

from app.database.models.user import User


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column()
    holder_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    holder: Mapped[User] = relationship(lazy="selectin")
