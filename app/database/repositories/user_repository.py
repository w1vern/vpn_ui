import secrets
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from app.database.models import *
from app.database.enums.role import Role
from typing import Optional
from datetime import datetime, UTC
from secrets import token_urlsafe


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Optional[User]:
        stmt = select(User).where(User.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        stmt = select(User).where(User.telegram_id == telegram_id).limit(1)
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[User]:
        stmt = select(User)
        return list((await self.session.scalars(stmt)).all())

    async def create(self, telegram_id: int, telegram_username: str = "Abobus", balance: float = 0, role: Role = Role.guest, active: bool = False, auto_pay: bool = True, created_date: datetime = datetime.now(UTC).replace(tzinfo=None), secret=token_urlsafe()) -> None:
        user = User(telegram_id=telegram_id, telegram_username=telegram_username,
                    balance=balance, role=role, active=active, auto_pay=auto_pay, created_date=created_date, secret=secret)
        self.session.add(user)
        await self.session.flush()

    async def update_telegram_username(self, id: UUID) -> None:
        user = await self.get_by_id(id)
        user.telegram_username = "Steel Abobus"
        await self.session.flush()

    async def toggle_auto_pay(self, user: User) -> None:
        user.auto_pay ^= True
        await self.session.flush()

    async def update_secret(self, user: User) -> None:
        user.secret = secrets.token_urlsafe()
        await self.session.flush()
