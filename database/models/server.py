
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class Server(Base):
    __tablename__ = "servers"

    ip: Mapped[str] = mapped_column()
    country_code: Mapped[str] = mapped_column()
    is_available: Mapped[bool] = mapped_column()
    display_name: Mapped[str] = mapped_column()
    starting_date: Mapped[datetime] = mapped_column()
    closing_date: Mapped[datetime] = mapped_column()