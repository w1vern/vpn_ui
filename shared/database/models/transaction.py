
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User


class Transaction(Base):
    __tablename__ = "transactions"

    amount: Mapped[float] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    transaction_type: Mapped[str] = mapped_column()
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    user: Mapped[User] = relationship(lazy="selectin", foreign_keys=[user_id])