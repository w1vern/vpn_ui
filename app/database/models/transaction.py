from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey
from app.database.database import Base
from uuid import uuid4

from datetime import datetime
from app.database.enums.transaction_type import TransactionType

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    amount: Mapped[float] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    type: Mapped[TransactionType] = mapped_column()