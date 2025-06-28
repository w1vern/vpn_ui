

from datetime import timedelta

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base


class Tariff(Base):
    __tablename__ = "tariffs"

    name: Mapped[str] = mapped_column(unique=True)
    duration: Mapped[timedelta] = mapped_column()
    price: Mapped[float] = mapped_column()
    price_of_traffic_reset: Mapped[float] = mapped_column()
    traffic: Mapped[int] = mapped_column()

    is_special: Mapped[bool] = mapped_column()
