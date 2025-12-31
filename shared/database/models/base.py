
from datetime import datetime
from typing import Any, TypeVar
from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from pydantic_core import core_schema


class Unset:
    _instance = None
    __slots__ = ()

    def __new__(cls) -> 'Unset':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "UNSET"

    def __bool__(self) -> bool:
        return False

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> core_schema.CoreSchema:
        def validate(value: Any) -> Any:
            if isinstance(value, cls):
                return value
            return value

        return core_schema.no_info_plain_validator_function(
            validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: None if isinstance(x, cls) else x,
                return_schema=core_schema.any_schema(),
            ),
        )


UNSET = Unset()


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        sort_order=-1
    )

    created_date: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    deleted_date: Mapped[datetime | None] = mapped_column(
        nullable=True,
        default=None
    )
