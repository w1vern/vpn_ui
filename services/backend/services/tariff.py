
from datetime import timedelta
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    UNSET,
    DefaultTariffs,
    TariffRepository,
    Unset,
    UserRepository
)

from ..depends import get_session, get_tariff_repo, get_user
from ..exceptions import (
    NotTariffEditorException,
    SendFeedbackToAdminException,
    TariffAlreadyExistsException,
    TariffNotFoundException
)
from ..schemas import (
    CreateTariffSchema,
    EditTariffSchema,
    TariffSchema,
    UserSchema
)


class TariffService:
    def __init__(
        self,
        session: AsyncSession,
        tr: TariffRepository,
        user_schema: UserSchema
    ) -> None:
        self.session = session
        self.tr = tr
        self.user_schema = user_schema

    @classmethod
    def depends(
        cls,
        session: AsyncSession = Depends(get_session),
        tr: TariffRepository = Depends(get_tariff_repo),
        user_schema: UserSchema = Depends(get_user)
    ) -> 'TariffService':
        return cls(session, tr, user_schema)

    async def all(self) -> list[TariffSchema]:
        return [TariffSchema.from_db(t) for t in await self.tr.get_all()]

    async def get(
        self,
        tariff_id: UUID
    ) -> TariffSchema:
        tariff = await self.tr.get_by_id(tariff_id)
        if tariff is None:
            raise TariffNotFoundException()
        return TariffSchema.from_db(tariff)

    async def create(
        self,
        create_tariff_schema: CreateTariffSchema
    ) -> TariffSchema:
        if self.user_schema.rights.is_tariffs_editor is False:
            raise NotTariffEditorException()
        if create_tariff_schema.name.startswith("archive."):
            raise TariffAlreadyExistsException()
        tariff = await self.tr.get_by_name(create_tariff_schema.name)
        if tariff is not None:
            raise TariffAlreadyExistsException()
        tariff = await self.tr.create(
            name=create_tariff_schema.name,
            duration=timedelta(seconds=create_tariff_schema.duration),
            price=create_tariff_schema.price,
            price_of_traffic_reset=create_tariff_schema.price_of_traffic_reset,
            traffic=create_tariff_schema.traffic,
            description=create_tariff_schema.description,
            with_access=create_tariff_schema.with_access,
            with_unavailable_inbounds=create_tariff_schema.with_unavailable_inbounds,
            is_special=create_tariff_schema.is_special
        )
        return TariffSchema.from_db(tariff)

    async def delete(
        self,
        tariff_id: UUID
    ) -> None:
        if self.user_schema.rights.is_tariffs_editor is False:
            raise NotTariffEditorException()
        tariff = await self.tr.get_by_id(tariff_id)
        if tariff is None:
            raise TariffNotFoundException()
        ur = UserRepository(self.session)
        users = await ur.get_all(tariff_id=tariff.id)
        default_tariff = await self.tr.get_by_id(UUID(int=DefaultTariffs.DEFAULT.value))
        if default_tariff is None:
            raise SendFeedbackToAdminException()
        for user in users:
            await ur.update_tariff(user, default_tariff)
        await self.tr.edit(tariff, name=f"archive.{tariff.name}.{tariff.id}")
        await self.tr.delete(tariff)

    async def edit(
        self,
        tariff_id: UUID,
        edited_tariff: EditTariffSchema
    ) -> TariffSchema:
        if self.user_schema.rights.is_tariffs_editor is False:
            raise NotTariffEditorException()
        tariff = await self.tr.get_by_id(tariff_id)
        if tariff is None:
            raise TariffNotFoundException()
        duration = timedelta(seconds=edited_tariff.duration) \
            if not isinstance(edited_tariff.duration, Unset) else UNSET
        await self.tr.edit(
            tariff,
            name=edited_tariff.name,
            duration=duration,
            price=edited_tariff.price,
            price_of_traffic_reset=edited_tariff.price_of_traffic_reset,
            traffic=edited_tariff.traffic,
            description=edited_tariff.description,
            with_unavailable_inbounds=edited_tariff.with_unavailable_inbounds,
            with_access=edited_tariff.with_access,
            is_special=edited_tariff.is_special
        )
        return TariffSchema.from_db(tariff)
