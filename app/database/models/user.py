from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey
from app.database.database import Base
from uuid import uuid4

from app.database.enums.role import Role

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    telegram_username: Mapped[str] = mapped_column(default="New Abobus")
    balance: Mapped[float] = mapped_column(default=0)
    role: Mapped[Role] = mapped_column(default=Role.guest)

    active: Mapped[bool] = mapped_column(default=False)
    auto_pay: Mapped[bool] = mapped_column(default=True)
