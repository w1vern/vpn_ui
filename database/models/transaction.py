from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey
from database.models.base import Base
from uuid import uuid4
import uuid
from datetime import datetime

from database.enums.transaction_type import TransactionType
from database.models.user import User

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    amount: Mapped[float] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    type: Mapped[TransactionType] = mapped_column()
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    user: Mapped[User] = relationship(lazy="selectin")