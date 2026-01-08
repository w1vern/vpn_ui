
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Server(Base):
    __tablename__ = "servers"

    ip: Mapped[str] = mapped_column(unique=True)
    secured: Mapped[bool] = mapped_column()
    panel_port: Mapped[int] = mapped_column()
    panel_web_path: Mapped[str] = mapped_column()
    panel_login: Mapped[str] = mapped_column()
    panel_password: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    country_code: Mapped[str] = mapped_column()
    display_name: Mapped[str] = mapped_column()

    starting_date: Mapped[datetime] = mapped_column()
    closing_date: Mapped[datetime] = mapped_column()

    @property
    def panel_url(self) -> str:
        return f"http{'s' * self.secured}://{self.ip}:{self.panel_port}/{self.panel_web_path}/"
