
import secrets
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from ..enums import (
    Rights,
    RightsType,
    Settings,
    SettingsType,
)
from ..models import (
    Tariff,
    User,
)
from .base import (
    BaseRepository,
)


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def create(self,
                     telegram_id: int,
                     telegram_username: str,
                     tariff_id: UUID,
                     balance: float = 0,
                     rights: int = RightsType.member.value,
                     settings: int = SettingsType.default.value,
                     ) -> User:
        return await self.universal_create(
            telegram_id=telegram_id,
            tariff_id=tariff_id,
            telegram_username=telegram_username,
            balance=balance,
            rights=rights,
            settings=settings)

    async def get_by_telegram_id(self,
                                 telegram_id: int
                                 ) -> User | None:
        stmt = select(User).where(
            User.telegram_id == telegram_id).limit(1)
        return await self.session.scalar(stmt)

    async def update_telegram_username(self,
                                       user: User,
                                       new_tg_username: str
                                       ) -> None:
        user.telegram_username = new_tg_username
        await self.session.flush()

    async def update_telegram_id(self,
                                 user: User,
                                 new_tg_id: int) -> None:
        user.telegram_id = new_tg_id
        await self.session.flush()

    async def update_balance(self,
                             user: User,
                             diff: float
                             ) -> None:
        user.balance += diff
        await self.session.flush()

    async def update_rights(self,
                            user: User,
                            updated_rights: dict[str, bool]
                            ) -> None:
        for right, value in updated_rights.items():
            if getattr(user, right) != value:
                user.rights ^= Rights(right).value
        await self.session.flush()

    async def update_settings(self,
                              user: User,
                              updated_settings: dict[str, bool]
                              ) -> None:
        for setting, value in updated_settings.items():
            if getattr(user, setting) != value:
                user.settings ^= Settings(setting).value
        await self.session.flush()

    async def update_secret(self, user: User) -> None:
        user.secret = secrets.token_urlsafe()
        await self.session.flush()

    async def update_tariff(self,
                            user: User,
                            new_tariff: Tariff
                            ) -> None:
        user.tariff_id = new_tariff.id
        await self.session.flush()
