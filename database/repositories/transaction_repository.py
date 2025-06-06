from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.enums.transaction_type import TransactionType
from database.models import *


class TransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self,
                     user: User,
                     amount: float,
                     date: datetime | None = None,
                     type: int = TransactionType.withdrawal.value
                     ) -> Transaction | None:
        if date is None:
            date = datetime.now(UTC).replace(tzinfo=None)
        transaction = Transaction(
            user_id=user.id, amount=amount, date=date, type=type)
        user.balance += amount
        self.session.add(transaction)
        await self.session.flush()
        return await self.get_by_id(transaction.id)

    async def get_by_id(self, id: UUID) -> Transaction | None:
        stmt = select(Transaction).where(Transaction.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[Transaction]:
        stmt = select(Transaction)
        return list((await self.session.scalars(stmt)).all())

    async def get_by_user(self, user: User) -> list[Transaction]:
        stmt = select(Transaction).where(Transaction.user_id == user.id)
        return list((await self.session.scalars(stmt)).all())
