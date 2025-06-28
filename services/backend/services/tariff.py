
from datetime import timedelta
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import TariffRepository

from ..exceptions import (
    NotTariffEditorException,
    TariffNotFoundException
)
from ..schemas import (
    CreateTariffSchema,
    EditTariffSchema,
    TariffSchema,
    UserSchema
)
from .depends import (
    get_session,
    get_tariff_repo,
    get_user,
)


class TariffService:
    def __init__(self,
                 session: AsyncSession,
                 tr: TariffRepository,
                 user_schema: UserSchema
                 ) -> None:
        self.session = session
        self.tr = tr
        self.user_schema = user_schema

    @classmethod
    def depends(cls,
                session: AsyncSession = Depends(get_session),
                tr: TariffRepository = Depends(get_tariff_repo),
                user_schema: UserSchema = Depends(get_user)
                ) -> 'TariffService':
        return cls(session, tr, user_schema)

    async def all(self) -> list[TariffSchema]:
        return [TariffSchema.from_db(t) for t in await self.tr.get_all()]

    async def get(self, tariff_id: UUID) -> TariffSchema:
        tariff = await self.tr.get_by_id(tariff_id)
        if tariff is None:
            raise TariffNotFoundException()
        return TariffSchema.from_db(tariff)

    async def create(self,
                     create_tariff_schema: CreateTariffSchema
                     ) -> None:
        if self.user_schema.rights.is_tariff_editor is False:
            raise NotTariffEditorException()
        await self.tr.create(
            name=create_tariff_schema.name,
            duration=timedelta(seconds=create_tariff_schema.duration),
            price=create_tariff_schema.price,
            price_of_traffic_reset=create_tariff_schema.price_of_traffic_reset,
            traffic=create_tariff_schema.traffic
        )

    async def delete(self, tariff_id: UUID) -> None:
        if self.user_schema.rights.is_tariff_editor is False:
            raise NotTariffEditorException()
        tariff = await self.tr.get_by_id(tariff_id)
        if tariff is None:
            raise TariffNotFoundException()
        await self.tr.delete(tariff)

    async def edit(self, tariff_id: UUID, edited_tariff: EditTariffSchema) -> None:
        if self.user_schema.rights.is_tariff_editor is False:
            raise NotTariffEditorException()
        tariff = await self.tr.get_by_id(tariff_id)
        if tariff is None:
            raise TariffNotFoundException()
        duration = timedelta(seconds=edited_tariff.duration) \
            if edited_tariff.duration is not None else None
        await self.tr.edit(
            tariff,
            name=edited_tariff.name,
            duration=duration,
            price=edited_tariff.price,
            price_of_traffic_reset=edited_tariff.price_of_traffic_reset,
            traffic=edited_tariff.traffic
        )
