
from secrets import token_urlsafe
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..enums import Rights, Settings
from .base import Base
from .tariff import Tariff


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    tariff_id: Mapped[UUID] = mapped_column(ForeignKey("tariffs.id"))
    telegram_username: Mapped[str] = mapped_column()
    balance: Mapped[float] = mapped_column()
    rights: Mapped[int] = mapped_column()
    settings: Mapped[int] = mapped_column()
    secret: Mapped[str] = mapped_column(default=token_urlsafe)

    tariff: Mapped[Tariff] = relationship(
        lazy="selectin", foreign_keys=[tariff_id])

    @property
    def is_server_editor(self) -> bool:
        return self.rights & Rights.is_servers_editor.value != 0

    @is_server_editor.setter
    def is_server_editor(self, value: bool):
        if self.is_server_editor != value:
            self.rights ^= Rights.is_servers_editor.value

    @property
    def is_transaction_editor(self) -> bool:
        return self.rights & Rights.is_transactions_editor.value != 0

    @is_transaction_editor.setter
    def is_transaction_editor(self, value: bool):
        if self.is_transaction_editor != value:
            self.rights ^= Rights.is_transactions_editor.value

    @property
    def is_active_period_editor(self) -> bool:
        return self.rights & Rights.is_active_periods_editor.value != 0

    @is_active_period_editor.setter
    def is_active_period_editor(self, value: bool):
        if self.is_active_period_editor != value:
            self.rights ^= Rights.is_active_periods_editor.value

    @property
    def is_tariff_editor(self) -> bool:
        return self.rights & Rights.is_tariffs_editor.value != 0

    @is_tariff_editor.setter
    def is_tariff_editor(self, value: bool):
        if self.is_tariff_editor != value:
            self.rights ^= Rights.is_tariffs_editor.value

    @property
    def is_member_rights_editor(self) -> bool:
        return self.rights & Rights.is_member_rights_editor.value != 0

    @is_member_rights_editor.setter
    def is_member_rights_editor(self, value: bool):
        if self.is_member_rights_editor != value:
            self.rights ^= Rights.is_member_rights_editor.value

    @property
    def is_user_editor(self) -> bool:
        return self.rights & Rights.is_users_editor.value != 0

    @is_user_editor.setter
    def is_user_editor(self, value: bool):
        if self.is_user_editor != value:
            self.rights ^= Rights.is_users_editor.value

    @property
    def is_admin_rights_editor(self) -> bool:
        return self.rights & Rights.is_admin_rights_editor.value != 0

    @is_admin_rights_editor.setter
    def is_admin_rights_editor(self, value: bool):
        if self.is_admin_rights_editor != value:
            self.rights ^= Rights.is_admin_rights_editor.value

    @property
    def is_control_panel_user(self) -> bool:
        return self.rights & Rights.is_control_panel_user.value != 0

    @is_control_panel_user.setter
    def is_control_panel_user(self, value: bool):
        if self.is_control_panel_user != value:
            self.rights ^= Rights.is_control_panel_user.value

    @property
    def can_use(self) -> bool:
        return self.rights & Rights.can_use.value != 0

    @can_use.setter
    def can_use(self, value: bool):
        if self.can_use != value:
            self.rights ^= Rights.can_use.value

    @property
    def is_verified(self) -> bool:
        return self.rights & Rights.is_verified.value != 0

    @is_verified.setter
    def is_verified(self, value: bool):
        if self.is_verified != value:
            self.rights ^= Rights.is_verified.value

    @property
    def auto_pay(self) -> bool:
        return self.settings & Settings.auto_pay.value != 0

    @auto_pay.setter
    def auto_pay(self, value: bool):
        if self.auto_pay != value:
            self.settings ^= Settings.auto_pay.value

    @property
    def is_active(self) -> bool:
        return self.settings & Settings.is_active.value != 0

    @is_active.setter
    def is_active(self, value: bool):
        if self.is_active != value:
            self.settings ^= Settings.is_active.value

    @property
    def get_traffic_notifications(self) -> bool:
        return self.settings & Settings.get_traffic_notifications.value != 0

    @get_traffic_notifications.setter
    def get_traffic_notifications(self, value: bool):
        if self.get_traffic_notifications != value:
            self.settings ^= Settings.get_traffic_notifications.value
