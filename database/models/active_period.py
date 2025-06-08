from datetime import datetime
from uuid import UUID

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base
from database.models.tariff import Tariff
from database.models.transaction import Transaction
from database.models.user import User


class ActivePeriod(Base):
    __tablename__ = "active_periods"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    transaction_id: Mapped[UUID] = mapped_column(
        ForeignKey("transactions.id"))
    tariff_id: Mapped[UUID] = mapped_column(ForeignKey("tariffs.id"))
    start_date: Mapped[datetime] = mapped_column()
    end_date: Mapped[datetime] = mapped_column()
    result_traffic: Mapped[int] = mapped_column()
    opened: Mapped[bool] = mapped_column()

    user: Mapped[User] = relationship(
        lazy="selectin", foreign_keys=[user_id])
    transaction: Mapped[Transaction] = relationship(
        lazy="selectin", foreign_keys=[transaction_id])
    tariff: Mapped[Tariff] = relationship(
        lazy='selectin', foreign_keys=[tariff_id])
