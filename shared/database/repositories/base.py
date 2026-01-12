
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import BinaryExpression, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_

from ..models import UNSET, BaseModel, Unset

ModelType = TypeVar("ModelType", bound=BaseModel)



class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelType]
    ) -> None:
        self.session = session
        self.model = model

    async def _create(
        self,
        **kwargs: object
    ) -> ModelType:
        model = self.model(**kwargs)
        self.session.add(model)
        await self.session.flush()
        model = await self.get_by_id(model.id)
        if model is None:
            raise Exception("Model not created")
        return model
    
    async def _super_edit(
        self,
        obj: object,
        **kwargs: object | Unset 
    ) -> None:
        for field, value in kwargs.items():
            if value is not UNSET:
                if not hasattr(obj, field):
                    raise ValueError(
                        f"{self.model.__name__} has no attribute {field}")
                setattr(obj, field, value)
        await self.session.flush()

    async def _edit(
        self,
        instance: ModelType,
        **kwargs: object | Unset
    ) -> None:
        await self._super_edit(instance, **kwargs)

    async def get_by_id(
        self,
        id: UUID
    ) -> ModelType | None:
        stmt = select(self.model).where(
            self.model.id == id,
            self.model.deleted_date.is_(None)
        ).limit(1)
        return await self.session.scalar(stmt)

    def __build_filters(
        self,
        **kwargs: Any | None
    ) -> list[BinaryExpression[bool]]:
        filters = [self.model.deleted_date.is_(None)]
        for field, value in kwargs.items():
            if value is not None:
                if hasattr(self.model, field):
                    filters.append(getattr(self.model, field) == value)
                else:
                    raise ValueError(
                        f"Model {self.model.__name__} has no field '{field}'")
        return filters

    async def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None,
        /,
        **kwargs: object | None
    ) -> list[ModelType]:
        stmt = (
            select(self.model)
            .where(and_(*self.__build_filters(**kwargs)))
            .limit(limit)
            .offset(offset)
            .order_by(self.model.created_date.desc(), self.model.id.asc())
        )
        return list((await self.session.scalars(stmt)).all())

    async def count(
        self,
        **kwargs: object | None
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(self.model)
            .where(and_(*self.__build_filters(**kwargs)))
        )
        count = await self.session.scalar(stmt)
        if count is None:
            return 0
        return count

    async def delete(
        self,
        instance: ModelType
    ) -> None:
        instance.deleted_date = datetime.now(UTC).replace(tzinfo=None)
        await self.session.flush()
