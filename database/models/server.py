import uuid
from datetime import datetime
from uuid import uuid4

from pydantic import UUID4
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    ip: Mapped[str] = mapped_column()
    country_code: Mapped[str] = mapped_column()
    is_available: Mapped[bool] = mapped_column()
    display_name: Mapped[str] = mapped_column()
    created_date: Mapped[datetime] = mapped_column()
    closing_date: Mapped[datetime] = mapped_column()

    type: Mapped[str] = mapped_column()


    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "polymorphic_on": "type",
    }