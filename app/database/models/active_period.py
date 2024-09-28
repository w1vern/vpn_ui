from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey, func
from app.database.database import Base
from uuid import uuid4

from datetime import datetime

from app.database.models.user import User
from app.database.models.transaction import Transaction

class ActivePeriod(Base):
    __tablename__ = "active_periods"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    transaction_id: Mapped[UUID] = mapped_column(ForeignKey("transactions.id"))
    start_time: Mapped[datetime] = mapped_column(default=func.now())
    ending_time: Mapped[datetime] = mapped_column()

    user: Mapped[User] = relationship(lazy="selectin")
    transaction: Mapped[Transaction] = relationship(lazy="selectin")

