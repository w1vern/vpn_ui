from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import *

from datetime import datetime, UTC
from typing import Optional



class ActivePeriodRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User, transaction: Transaction, start_date: datetime = datetime.now(UTC), end_date: datetime = datetime.now(UTC)) -> None:
        active_period = ActivePeriod(
            user_id=user.id, transaction_id=transaction.id, start_date=start_date, end_date=end_date)
        self.session.add(active_period)
        await self.session.flush()

    async def get_by_id(self, id:UUID) -> Optional[ActivePeriod]:
        stmt = select(ActivePeriod).where(ActivePeriod.id == id).limit(1)
        return await self.session.scalar(stmt)
    
    async def get_by_user_id(self, user:User) -> list[ActivePeriod]:
        stmt = select(ActivePeriod).where(ActivePeriod.user_id == user.user_id)
        return list((await self.session.scalars(stmt)).all())
