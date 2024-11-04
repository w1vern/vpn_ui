from pydantic import UUID4
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.models.base import Base
from uuid import uuid4
import uuid

from database.enums.role import Role
from datetime import datetime


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=UUID4)
    ip: Mapped[str] = mapped_column()
    panel_path: Mapped[str] = mapped_column()
    country_code: Mapped[str] = mapped_column()
    is_available: Mapped[bool] = mapped_column()
    display_name: Mapped[str] = mapped_column()
    created_date: Mapped[datetime] = mapped_column()
    closing_date: Mapped[datetime] = mapped_column()
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
