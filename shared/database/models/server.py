
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Server(Base):
    __tablename__ = "servers"

    ip: Mapped[str] = mapped_column()
    secured: Mapped[bool] = mapped_column()
    panel_port: Mapped[int] = mapped_column()
    web_path: Mapped[str] = mapped_column()
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    country_code: Mapped[str] = mapped_column()
    display_name: Mapped[str] = mapped_column()
