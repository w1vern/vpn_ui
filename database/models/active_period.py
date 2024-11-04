from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey
from database.models.base import Base
from uuid import uuid4
import uuid
from datetime import datetime

from database.models.user import User
from database.models.transaction import Transaction

class ActivePeriod(Base):
    __tablename__ = "active_periods"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    transaction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("transactions.id"))
    start_date: Mapped[datetime] = mapped_column()
    end_date: Mapped[datetime] = mapped_column()

    user: Mapped[User] = relationship(lazy="selectin")
    transaction: Mapped[Transaction] = relationship(lazy="selectin")

