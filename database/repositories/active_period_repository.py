from datetime import UTC, datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import *


class ActivePeriodRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User, transaction: Transaction, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Optional[ActivePeriod]:
        if start_date is None:
            start_date = datetime.now(UTC).replace(tzinfo=None)
        if end_date is None:
            end_date = datetime.now(UTC).replace(tzinfo=None) + timedelta(days=1)
        active_period = ActivePeriod(
            user_id=user.id, transaction_id=transaction.id, start_date=start_date, end_date=end_date)
        self.session.add(active_period)
        await self.session.flush()
        return await self.get_by_id(active_period.id)

    async def get_by_id(self, id: UUID) -> Optional[ActivePeriod]:
        stmt = select(ActivePeriod).where(ActivePeriod.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_user_id(self, user: User) -> list[ActivePeriod]:
        stmt = select(ActivePeriod).where(ActivePeriod.user_id == user.id)
        return list((await self.session.scalars(stmt)).all())
