import secrets
from datetime import UTC, datetime
from secrets import token_urlsafe
from uuid import UUID

from httpx import get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.enums.rights import Rights
from database.enums.rights_type import RightsType
from database.enums.settings import Settings
from database.enums.settings_type import SettingsType
from database.models import *
from database.models.tariff import Tariff


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self,
                     telegram_id: str,
                     telegram_username: str,
                     tariff_id: UUID,
                     balance: float = 0,
                     rights: int = RightsType.member.value,
                     settings: int = SettingsType.default.value,
                     created_date: datetime | None = None,
                     secret: str | None = None
                     ) -> User | None:
        if created_date is None:
            created_date = datetime.now(UTC).replace(tzinfo=None)
        if secret is None:
            secret = secrets.token_urlsafe()
        user = User(telegram_id=telegram_id,
                    tariff_id=tariff_id,
                    telegram_username=telegram_username,
                    balance=balance,
                    rights=rights,
                    settings=settings,
                    created_date=created_date,
                    secret=secret)
        self.session.add(user)
        await self.session.flush()
        return await self.get_by_id(user.id)

    async def get_by_id(self, id: UUID) -> User | None:
        stmt = select(User).where(User.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_telegram_id(self, telegram_id: str) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id).limit(1)
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[User]:
        stmt = select(User)
        return list((await self.session.scalars(stmt)).all())

    async def update_telegram_username(self, user: User, new_tg_username: str) -> None:
        user.telegram_username = new_tg_username
        await self.session.flush()

    async def update_telegram_id(self, user: User, new_tg_id: str) -> None:
        user.telegram_id = new_tg_id
        await self.session.flush()

    async def update_created_date(self, user: User, new_created_date: datetime) -> None:
        user.created_date = new_created_date
        await self.session.flush()

    async def update_balance(self, user: User, diff: float) -> None:
        user.balance += diff
        await self.session.flush()


    async def update_rights(self, user: User, updated_rights: dict[str, bool]) -> None:
        for right, value in updated_rights.items():
            if getattr(user, right) != value:
                user.rights ^= Rights(right).value
        await self.session.flush()

    async def update_settings(self, user: User, updated_settings: dict[str, bool]) -> None:
        for setting, value in updated_settings.items():
            if getattr(user, setting) != value:
                user.settings ^= Settings(setting).value
        await self.session.flush()

    async def update_secret(self, user: User) -> None:
        user.secret = secrets.token_urlsafe()
        await self.session.flush()

    async def update_tariff(self, user: User, new_tariff: Tariff) -> None:
        user.tariff_id = new_tariff.id
        await self.session.flush()
