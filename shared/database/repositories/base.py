

from datetime import UTC, datetime
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
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

    async def get_all(self) -> list[ModelType]:
        stmt = select(self.model).where(self.model.deleted_date == None)
        return list((await self.session.scalars(stmt)).all())

    async def get_all_filtered(self, **kwargs) -> list[ModelType]:
        stmt = select(self.model).where(
            self.model.deleted_date == None, **kwargs)
        return list((await self.session.scalars(stmt)).all())

    async def delete(self, instance: ModelType) -> None:
        instance.deleted_date = datetime.now(UTC).replace(tzinfo=None)
        await self.session.flush()
