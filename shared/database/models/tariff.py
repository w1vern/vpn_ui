
from datetime import timedelta

from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Tariff(BaseModel):
    __tablename__ = "tariffs"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    duration: Mapped[timedelta] = mapped_column()
    price: Mapped[float] = mapped_column()
    price_of_traffic_reset: Mapped[float] = mapped_column()
    traffic: Mapped[int] = mapped_column()

    with_access: Mapped[bool] = mapped_column()
    with_unavailable_inbounds: Mapped[bool] = mapped_column()
    is_special: Mapped[bool] = mapped_column()
