
from datetime import timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UNSET, Tariff, Unset
from .base import BaseRepository


class TariffRepository(BaseRepository[Tariff]):
    def __init__(
        self,
        session: AsyncSession
    ) -> None:
        super().__init__(session, Tariff)

    async def create(
        self,
        name: str,
        duration: timedelta,
        price: int,
        price_of_traffic_reset: int,
        traffic: int,
        description: str,
        with_access: bool,
        with_unavailable_inbounds: bool,
        is_special: bool,
        id: UUID | None = None
    ) -> Tariff:
        id_kwarg = {"id": id} if id is not None else {}
        return await self._create(
            name=name,
            duration=duration,
            description=description,
            price=price,
            price_of_traffic_reset=price_of_traffic_reset,
            traffic=traffic,
            with_access=with_access,
            with_unavailable_inbounds=with_unavailable_inbounds,
            is_special=is_special,
            **id_kwarg
        )

    async def edit(
        self,
        tariff: Tariff,
        *,
        name: str | Unset = UNSET,
        description: str | Unset = UNSET,
        duration: timedelta | Unset = UNSET,
        price: int | Unset = UNSET,
        price_of_traffic_reset: int | Unset = UNSET,
        traffic: int | Unset = UNSET,
        with_access: bool | Unset = UNSET,
        with_unavailable_inbounds: bool | Unset = UNSET,
        is_special: bool | Unset = UNSET
    ) -> None:
        await self._edit(
            tariff,
            name=name,
            description=description,
            duration=duration,
            price=price,
            price_of_traffic_reset=price_of_traffic_reset,
            traffic=traffic,
            with_access=with_access,
            with_unavailable_inbounds=with_unavailable_inbounds,
            is_special=is_special
        )

    async def get_by_name(
        self,
        name: str
    ) -> Tariff | None:
        stmt = select(Tariff).where(Tariff.name == name).limit(1)
        return await self.session.scalar(stmt)
