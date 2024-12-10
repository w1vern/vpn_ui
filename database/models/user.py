import uuid
from datetime import datetime
from uuid import uuid4

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.enums.rights import Rights
from database.enums.settings import Settings
from database.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    telegram_id: Mapped[str] = mapped_column(unique=True, index=True)
    telegram_username: Mapped[str] = mapped_column()
    balance: Mapped[float] = mapped_column()
    rights: Mapped[int] = mapped_column()
    settings: Mapped[int] = mapped_column()
    created_date: Mapped[datetime] = mapped_column()
    secret: Mapped[str] = mapped_column()

    @property
    def is_server_editor(self) -> bool:
        return self.rights & Rights.edit_servers.value != 0

    @property
    def is_transaction_editor(self) -> bool:
        return self.rights & Rights.edit_transactions.value != 0

    @property
    def is_active_period_editor(self) -> bool:
        return self.rights & Rights.edit_active_periods.value != 0

    @property
    def is_tariff_editor(self) -> bool:
        return self.rights & Rights.edit_tariffs.value != 0

    @property
    def is_member_rights_editor(self) -> bool:
        return self.rights & Rights.edit_member_rights.value != 0
    
    @property 
    def is_user_editor(self) -> bool:
        return self.rights & Rights.edit_users.value != 0

    @property
    def is_admin_rights_editor(self) -> bool:
        return self.rights & Rights.edit_admin_rights.value != 0

    @property
    def is_control_panel_user(self) -> bool:
        return self.rights & Rights.use_control_panel.value != 0

    @property
    def is_active(self) -> bool:
        return self.rights & Rights.active.value != 0

    @property
    def verified(self) -> bool:
        return self.rights & Rights.verified.value != 0

    @property
    def auto_pay(self) -> bool:
        return self.settings & Settings.auto_pay.value != 0
