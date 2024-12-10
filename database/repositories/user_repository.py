import secrets
from datetime import UTC, datetime
from secrets import token_urlsafe
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.enums.rights import Rights
from database.enums.rights_type import RightsType
from database.enums.settings import Settings
from database.enums.settings_type import SettingsType
from database.models import *


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self,
                     telegram_id: int,
                     telegram_username: str,
                     balance: float = 0,
                     rights: int = RightsType.member.value,
                     settings: int = SettingsType.default.value,
                     created_date: Optional[datetime] = None,
                     secret: Optional[str] = None
                     ) -> Optional[User]:
        if created_date is None:
            created_date = datetime.now(UTC).replace(tzinfo=None)
        if secret is None:
            secret = secrets.token_urlsafe()
        user = User(telegram_id=telegram_id,
                    telegram_username=telegram_username,
                    balance=balance,
                    rights=rights,
                    settings=settings,
                    created_date=created_date,
                    secret=secret)
        self.session.add(user)
        await self.session.flush()
        return await self.get_by_id(user.id)

    async def get_by_id(self, id: UUID) -> Optional[User]:
        stmt = select(User).where(User.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        stmt = select(User).where(User.telegram_id == telegram_id).limit(1)
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[User]:
        stmt = select(User)
        return list((await self.session.scalars(stmt)).all())

    async def update_telegram_username(self, user: User, new_tg_username: str) -> None:
        user.telegram_username = new_tg_username
        await self.session.flush()

    async def toggle_auto_pay(self, user: User) -> None:
        user.settings ^= Settings.auto_pay.value
        await self.session.flush()

    async def update_secret(self, user: User) -> None:
        user.secret = secrets.token_urlsafe()
        await self.session.flush()
