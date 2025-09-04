

from datetime import (
    UTC,
    datetime,
)
from typing import (
    Generic,
    TypeVar,
)
from uuid import UUID

from sqlalchemy import BinaryExpression, func, select
from sqlalchemy.sql import and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self,
                 session: AsyncSession,
                 model: type[ModelType]
                 ) -> None:
        self.session = session
        self.model = model

    async def universal_create(self, **kwargs) -> ModelType:
        model = self.model(**kwargs)
        self.session.add(model)
        await self.session.flush()
        model = await self.get_by_id(model.id)
        if model is None:
            raise Exception("Model not created")
        return model

    async def get_by_id(self, id: UUID) -> ModelType | None:
        stmt = select(self.model).where(
            self.model.id == id,
            self.model.deleted_date == None
        ).limit(1)
        return await self.session.scalar(stmt)

    def _build_filters(self, **kwargs) -> list[BinaryExpression]:
        filters = [self.model.deleted_date.is_(None)]
        for field, value in kwargs.items():
            if hasattr(self.model, field):
                filters.append(getattr(self.model, field) == value)
            else:
                raise ValueError(
                    f"Model {self.model.__name__} has no field '{field}'")
        return filters

    async def get_all(self,
                      limit: int | None = None,
                      offset: int | None = None,
                      **kwargs
                      ) -> list[ModelType]:
        stmt = (
            select(self.model)
            .where(and_(*self._build_filters(**kwargs)))
            .limit(limit)
            .offset(offset)
        )
        return list((await self.session.scalars(stmt)).all())

    async def count(self, **kwargs) -> int:
        stmt = (
            select(func.count())
            .select_from(self.model)
            .where(and_(*self._build_filters(**kwargs)))
        )
        count = await self.session.scalar(stmt)
        if count is None:
            return 0
        return count

    async def delete(self, instance: ModelType) -> None:
        instance.deleted_date = datetime.now(UTC).replace(tzinfo=None)
        await self.session.flush()
