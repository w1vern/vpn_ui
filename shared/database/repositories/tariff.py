

from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Tariff
from .base import BaseRepository


class TariffRepository(BaseRepository[Tariff]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Tariff)

    async def create(self,
                     name: str,
                     duration: timedelta,
                     price: float,
                     price_of_traffic_reset: float,
                     traffic: int,
                     is_special: bool = False
                     ) -> Tariff:
        return await self.universal_create(
            name=name,
            duration=duration,
            price=price,
            price_of_traffic_reset=price_of_traffic_reset,
            traffic=traffic,
            is_special=is_special
        )

    async def edit(self,
                   tariff: Tariff,
                   name: str | None = None,
                   duration: timedelta | None = None,
                   price: float | None = None,
                   price_of_traffic_reset: float | None = None,
                   traffic: int | None = None,
                   is_special: bool | None = None
                   ) -> None:
        if name is not None:
            tariff.name = name
        if duration is not None:
            tariff.duration = duration
        if price is not None:
            tariff.price = price
        if price_of_traffic_reset is not None:
            tariff.price_of_traffic_reset = price_of_traffic_reset
        if traffic is not None:
            tariff.traffic = traffic
        if is_special is not None:
            tariff.is_special = is_special
        await self.session.flush()
        

    async def get_by_name(self, name: str) -> Tariff | None:
        stmt = select(Tariff).where(Tariff.name == name).limit(1)
        return await self.session.scalar(stmt)
