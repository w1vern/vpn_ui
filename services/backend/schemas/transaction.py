

from uuid import UUID

from pydantic import BaseModel

from shared.database import Transaction


class TransactionSchema(BaseModel):
    user_id: UUID
    amount: float
    transaction_type: str
    date: str | None = None

    @classmethod
    def from_db(cls,
                transaction: Transaction
                ) -> "TransactionSchema":
        return cls(
            user_id=transaction.user_id,
            amount=transaction.amount,
            transaction_type=transaction.transaction_type,
            date=transaction.date.isoformat()
        )
