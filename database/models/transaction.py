import uuid
from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.enums.transaction_type import TransactionType
from database.models.base import Base
from database.models.user import User


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    amount: Mapped[float] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    type: Mapped[TransactionType] = mapped_column()
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    user: Mapped[User] = relationship(lazy="selectin", foreign_keys=[user_id])