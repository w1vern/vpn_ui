from sqlalchemy.orm import Session
from sqlalchemy import UUID, select
from app.database.models import *
from app.database.enums.role import Role
from typing import Optional
from datetime import datetime, UTC


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, id: UUID) -> Optional[User]:
        stmt = select(User).where(User.id == id).limit(1)
        return self.session.scalar(stmt)

    def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        stmt = select(User).where(User.telegram_id == telegram_id).limit(1)
        return self.session.scalar(stmt)

    def get_all(self) -> list[User]:
        stmt = select(User)
        return list(self.session.scalars(stmt).all())

    def create(self, telegram_id: int, telegram_username: str = "Abobus", balance: float = 0, role: Role = Role.guest, active: bool = False, auto_pay: bool = True, created_date: datetime = datetime.now(UTC)) -> None:
        user = User(telegram_id=telegram_id, telegram_username=telegram_username,
                    balance=balance, role=role, active=active, auto_pay=auto_pay, created_date=created_date)
        self.session.add(user)
        self.session.flush()

    def set_telegram_username(self, id: UUID) -> None:
        user = self.get_by_id(id)
        user.telegram_username = "Steel Abobus"
        self.session.flush()

    def toggle_auto_pay(self, telegram_id: int) -> None:
       user = self.get_by_telegram_id(telegram_id)
       user.auto_pay ^= True
       self.session.flush()
