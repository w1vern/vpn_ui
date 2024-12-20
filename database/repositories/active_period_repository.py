import uuid
from datetime import UTC, datetime, timedelta
from typing import Optional
from unittest import result

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import *
from database.models.tariff import Tariff


class ActivePeriodRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User,
                     transaction: Transaction,
                     tariff: Tariff,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None,
                     result_traffic: int = -1,
                     ) -> Optional[ActivePeriod]:
        if start_date is None:
            start_date = datetime.now(UTC).replace(tzinfo=None)
        if end_date is None:
            end_date = datetime.min
        active_period = ActivePeriod(user_id=user.id,
                                     transaction_id=transaction.id,
                                     tariff_id=tariff.id,
                                     start_date=start_date,
                                     end_date=end_date,
                                     result_traffic=result_traffic)
        self.session.add(active_period)
        await self.session.flush()
        return await self.get_by_id(active_period.id)

    async def get_by_id(self, id: uuid.UUID) -> Optional[ActivePeriod]:
        stmt = select(ActivePeriod).where(ActivePeriod.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_user_id(self, user: User) -> list[ActivePeriod]:
        stmt = select(ActivePeriod).where(ActivePeriod.user_id == user.id)
        return list((await self.session.scalars(stmt)).all())

    async def get_last_by_user_id(self, user: User) -> Optional[ActivePeriod]:
        stmt = select(ActivePeriod).where(ActivePeriod.user_id ==
                                          user.id).order_by(ActivePeriod.end_date.desc()).limit(1)
        return await self.session.scalar(stmt)

    async def get_latest_for_user(self, user: User) -> Optional[ActivePeriod]:
        all = await self.get_by_user_id(user)
        if len(all) == 0:
            return None
        id = uuid.UUID(int=0)
        max_date = all[0].start_date
        for ap in all:
            if ap.start_date > max_date:
                max_date = ap.start_date
                id = ap.id
        return await self.get_by_id(id)

    async def close_period(self, active_period: ActivePeriod, all_traffic: int, end_date: Optional[datetime] = None) -> None:
        if end_date is not None:
            active_period.end_date = end_date
        active_period.end_date = datetime.now(UTC).replace(tzinfo=None)
        active_period.result_traffic = all_traffic
        await self.session.flush()
