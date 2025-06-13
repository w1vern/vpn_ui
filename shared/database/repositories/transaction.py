
from datetime import (
    UTC,
    datetime,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from ..enums import (
    TransactionType,
)
from ..models import (
    Transaction,
    User,
)
from .base import (
    BaseRepository,
)


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Transaction)

    async def create(self,
                     user: User,
                     amount: float,
                     date: datetime | None = None,
                     transaction_type: str = TransactionType.withdrawal.value
                     ) -> Transaction:
        if date is None:
            date = datetime.now(UTC).replace(tzinfo=None)
        return await self.universal_create(
            user_id=user.id,
            amount=amount,
            date=date,
            transaction_type=transaction_type)

    async def get_by_user(self,
                          user: User
                          ) -> list[Transaction]:
        stmt = select(Transaction).where(
            Transaction.user_id == user.id)
        return list((await self.session.scalars(stmt)).all())
