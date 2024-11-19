import uuid
from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base
from database.models.transaction import Transaction
from database.models.user import User


class ActivePeriod(Base):
    __tablename__ = "active_periods"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    transaction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("transactions.id"))
    start_date: Mapped[datetime] = mapped_column()
    end_date: Mapped[datetime] = mapped_column()

    user: Mapped[User] = relationship(lazy="selectin")
    transaction: Mapped[Transaction] = relationship(lazy="selectin")

