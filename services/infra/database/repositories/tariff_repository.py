

from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Tariff

from .base_repository import BaseRepository


class TariffRepository(BaseRepository[Tariff]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Tariff)

    async def create(self,
                     name: str,
                     duration: timedelta,
                     price: float,
                     price_of_traffic_reset: float,
                     traffic: int
                     ) -> Tariff:
        return await self.universal_create(
            name=name,
            duration=duration,
            price=price,
            price_of_traffic_reset=price_of_traffic_reset,
            traffic=traffic)

    async def get_by_name(self, name: str) -> Tariff | None:
        stmt = select(Tariff).where(Tariff.name == name).limit(1)
        return await self.session.scalar(stmt)
