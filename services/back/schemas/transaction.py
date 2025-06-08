



from pydantic import BaseModel


class Transaction(BaseModel):
    user_id: str
    amount: float
    type: str
    date: str | None
