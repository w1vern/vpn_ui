

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from shared.database import Transaction, TransactionType


class TransactionSchema(BaseModel):
    user_id: UUID
    amount: float
    description: str
    transaction_type: TransactionType
    date: datetime | None = None

    @classmethod
    def from_db(cls,
                transaction: Transaction
                ) -> "TransactionSchema":
        return cls(
            user_id=transaction.user_id,
            description=transaction.description,
            amount=transaction.amount,
            transaction_type=TransactionType(transaction.transaction_type),
            date=transaction.date
        )
