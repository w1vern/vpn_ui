from sqlalchemy.orm import Session
from sqlalchemy import UUID, select

from app.database.models.transaction import Transaction
from app.database.enums.transaction_type import TransactionType
from typing import Optional
from datetime import datetime, UTC


class TransactionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, user_id: UUID, amount: float = 4, date: datetime = datetime.now(UTC), type: TransactionType = TransactionType.withdrawal) -> None:
        transaction = Transaction(
            user_id=user_id, amount=amount, date=date, type=type)
        self.session.add(transaction)
        self.session.flush()

    def get_by_id(self, id: UUID) -> Optional[Transaction]:
        stmt = select(Transaction).where(Transaction.id == id).limit(1)
        return self.session.scalar(stmt)

    def get_all(self) -> list[Transaction]:
        stmt = select(Transaction)
        return list(self.session.scalars(stmt).all)
    
    def get_by_user_id(self, user_id: UUID) -> list[Transaction]:
        stmt = select(Transaction).where(Transaction.user_id==user_id)
        return list(self.session.scalars(stmt).all())
