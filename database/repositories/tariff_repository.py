

import uuid
from datetime import timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.tariff import Tariff


class TrafficRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,
                     duration: timedelta,
                     price: float,
                     all_traffic: int
                     ) -> Optional[Tariff]:
        tariff = Tariff(duration=duration, price=price,
                        all_traffic=all_traffic)
        self.session.add(tariff)
        await self.session.flush()
        return await self.get_by_id(tariff.id)

    async def get_by_id(self, id: uuid.UUID) -> Optional[Tariff]:
        stmt = select(Tariff).where(Tariff.id == id).limit(1)
        return await self.session.scalar(stmt)
