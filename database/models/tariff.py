

import uuid
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timedelta

class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    duration: Mapped[timedelta] = mapped_column()
    price: Mapped[float] = mapped_column()
    all_traffic: Mapped[int] = mapped_column()
    traffic_by_server: Mapped[int] = mapped_column()