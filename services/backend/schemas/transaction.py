

from pydantic import BaseModel


class TransactionSchema(BaseModel):
    user_id: str
    amount: float
    transaction_type: str
    date: str | None = None
