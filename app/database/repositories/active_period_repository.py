from sqlalchemy.orm import Session
from sqlalchemy import UUID, select

from app.database.models.active_period import ActivePeriod

from datetime import datetime, UTC
from typing import Optional


class ActivePeriodRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, user_id: UUID, transaction_id: UUID, start_date: datetime = datetime.now(UTC), end_date: datetime = datetime.now(UTC)) -> None:
        active_period = ActivePeriod(
            user_id=user_id, transaction_id=transaction_id, start_date=start_date, end_date=end_date)
        self.session.add(active_period)
        self.session.flush()

    def get_by_id(self, id:UUID) -> Optional[ActivePeriod]:
        stmt = select(ActivePeriod).where(ActivePeriod.id == id).limit(1)
        return self.session.scalar(stmt)
    
    def get_by_user_id(self, user_id:UUID) -> list[ActivePeriod]:
        stmt = select(ActivePeriod).where(ActivePeriod.user_id == user_id)
        return list(self.session.scalars(stmt).all())
