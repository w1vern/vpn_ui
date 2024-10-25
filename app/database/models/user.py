from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import BigInteger
from app.database.models.base import Base
from uuid import uuid4
import uuid

from app.database.enums.role import Role
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    telegram_id: Mapped[int] = mapped_column(type_=BigInteger, unique=True, index=True)
    telegram_username: Mapped[str] = mapped_column()
    balance: Mapped[float] = mapped_column()
    role: Mapped[Role] = mapped_column()
    active: Mapped[bool] = mapped_column()
    auto_pay: Mapped[bool] = mapped_column()
    created_date: Mapped[datetime] = mapped_column()
    secret: Mapped[str] = mapped_column()
