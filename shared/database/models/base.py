
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)
from sqlalchemy.sql import func

from typing import TypeVar


class Unset:
    _instance = None

    def __new__(cls) -> 'Unset':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "UNSET"

    def __bool__(self) -> bool:
        return False


UNSET = Unset()


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    created_date: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    deleted_date: Mapped[datetime | None] = mapped_column(
        nullable=True,
        default=None
    )
