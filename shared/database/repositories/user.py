
import secrets
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.enums import language_code

from ..models import (
    UNSET,
    Tariff,
    Unset,
    User,
    UserRights,
    UserSettings
)
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def create(
        self,
        *,
        telegram_id: int,
        telegram_username: str,
        description: str,
        tariff: Tariff,
        internal_id: str,
        balance: int,
        rights: UserRights,
        settings: UserSettings
    ) -> User:
        return await self._create(
            telegram_id=telegram_id,
            tariff_id=tariff.id,
            description=description,
            telegram_username=telegram_username,
            internal_id=internal_id,
            panel_id=uuid4(),
            balance=balance,
            rights=rights,
            settings=settings,
            secret=secrets.token_urlsafe(),
        )

    async def get_by_telegram_id(
        self,
        telegram_id: int
    ) -> User | None:
        stmt = select(User).where(
            User.telegram_id == telegram_id).limit(1)
        return await self.session.scalar(stmt)

    async def update_telegram_username(
        self,
        user: User,
        new_tg_username: str
    ) -> None:
        user.telegram_username = new_tg_username
        await self.session.flush()

    async def update_telegram_id(
        self,
        user: User,
        new_tg_id: int
    ) -> None:
        user.telegram_id = new_tg_id
        await self.session.flush()

    async def update_balance(
        self,
        user: User,
        diff: int
    ) -> None:
        user.balance += diff
        await self.session.flush()

    async def update_rights(
        self,
        user: User,
        *,
        is_admin_rights_editor: bool | Unset = UNSET,
        is_member_rights_editor: bool | Unset = UNSET,
        is_users_editor: bool | Unset = UNSET,
        is_servers_editor: bool | Unset = UNSET,
        is_control_panel_user: bool | Unset = UNSET,
        is_verified: bool | Unset = UNSET,
        is_transactions_editor: bool | Unset = UNSET,
        is_tariffs_editor: bool | Unset = UNSET
    ) -> None:
        await self._super_edit(
            obj=user.rights,
            is_admin_rights_editor=is_admin_rights_editor,
            is_member_rights_editor=is_member_rights_editor,
            is_users_editor=is_users_editor,
            is_servers_editor=is_servers_editor,
            is_control_panel_user=is_control_panel_user,
            is_verified=is_verified,
            is_transactions_editor=is_transactions_editor,
            is_tariffs_editor=is_tariffs_editor
        )

    async def update_settings(
        self,
        user: User,
        *,
        get_traffic_notifications: bool | Unset = UNSET,
        auto_pay: bool | Unset = UNSET,
        is_active: bool | Unset = UNSET,
        language_code: str | Unset = UNSET
    ) -> None:
        await self._super_edit(
            obj=user.settings,
            get_traffic_notifications=get_traffic_notifications,
            auto_pay=auto_pay,
            is_active=is_active,
            language_code=language_code
        )

    async def update_secret(
        self,
        user: User
    ) -> None:
        user.secret = secrets.token_urlsafe()
        await self.session.flush()

    async def update_panel_id(
        self,
        user: User
    ) -> None:
        user.panel_id = uuid4()
        await self.session.flush()

    async def update_tariff(
        self,
        user: User,
        new_tariff: Tariff
    ) -> None:
        user.tariff_id = new_tariff.id
        await self.session.flush()

    async def update_description(
        self,
        user: User,
        new_description: str
    ) -> None:
        user.description = new_description
        await self.session.flush()

    async def update_internal_id(
        self,
        user: User,
        new_internal_id: str
    ) -> None:
        user.internal_id = new_internal_id
        await self.session.flush()
