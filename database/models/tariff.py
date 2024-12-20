

import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    duration: Mapped[timedelta] = mapped_column()
    price: Mapped[float] = mapped_column()
    price_of_traffic_reset: Mapped[float] = mapped_column()
    traffic: Mapped[int] = mapped_column()
