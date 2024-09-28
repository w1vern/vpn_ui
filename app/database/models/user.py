from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey
from app.database.database import Base
from uuid import uuid4

from app.database.enums.role import Role

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    telegram_username: Mapped[str] = mapped_column(unique=True)
    balance: Mapped[float] = mapped_column(default=0)
    role: Mapped[Role] = mapped_column()

    active: Mapped[bool] = mapped_column()
    auto_pay: Mapped[bool] = mapped_column()
