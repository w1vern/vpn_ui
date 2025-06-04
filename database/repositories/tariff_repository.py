

import uuid
from datetime import timedelta


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.tariff import Tariff


class TariffRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,
                     name: str,
                     duration: timedelta,
                     price: float,
                     price_of_traffic_reset: float,
                     traffic: int
                     ) -> Tariff | None:
        tariff = Tariff(name=name, duration=duration, price=price, price_of_traffic_reset=price_of_traffic_reset,
                        traffic=traffic)
        self.session.add(tariff)
        await self.session.flush()
        return await self.get_by_id(tariff.id)

    async def get_by_id(self, id: uuid.UUID) -> Tariff | None:
        stmt = select(Tariff).where(Tariff.id == id).limit(1)
        return await self.session.scalar(stmt)
