
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from shared.database import UNSET, LanguageCodes, Unset, User

from .tariff import TariffSchema


class UserSettingsSchema(BaseModel):
    auto_pay: bool
    is_active: bool
    get_traffic_notifications: bool

    model_config = ConfigDict(from_attributes=True)


class UserRightsSchema(BaseModel):
    is_server_editor: bool
    is_user_editor: bool
    is_transaction_editor: bool
    is_active_period_editor: bool
    is_tariff_editor: bool
    is_member_rights_editor: bool
    is_admin_rights_editor: bool
    is_control_panel_user: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    id: UUID
    telegram_id: int
    telegram_username: str
    telegram_language_code: LanguageCodes
    description: str
    balance: float
    created_date: datetime
    rights: UserRightsSchema
    settings: UserSettingsSchema

    tariff: TariffSchema

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_db(cls, user: User) -> 'UserSchema':
        settings = UserSettingsSchema.model_validate(user)
        rights = UserRightsSchema.model_validate(user)
        return UserSchema(
            id=user.id,
            tariff=TariffSchema.from_db(user.tariff),
            telegram_id=user.telegram_id,
            telegram_username=user.telegram_username,
            telegram_language_code=LanguageCodes(user.telegram_language_code),
            balance=user.balance,
            created_date=user.created_date,
            description=user.description,
            rights=rights,
            settings=settings
        )


class EditUserSettingsSchema(BaseModel):
    auto_pay: bool | Unset = UNSET
    is_active: bool | Unset = UNSET
    get_traffic_notifications: bool | Unset = UNSET


class EditUserRightsSchema(BaseModel):
    is_server_editor: bool | Unset = UNSET
    is_user_editor: bool | Unset = UNSET
    is_transaction_editor: bool | Unset = UNSET
    is_active_period_editor: bool | Unset = UNSET
    is_tariff_editor: bool | Unset = UNSET
    is_member_rights_editor: bool | Unset = UNSET
    is_admin_rights_editor: bool | Unset = UNSET
    is_control_panel_user: bool | Unset = UNSET
    is_verified: bool | Unset = UNSET


class EditUserSchema(BaseModel):
    telegram_id: int | Unset = UNSET
    tariff_id: UUID | Unset = UNSET
    description: str | Unset = UNSET
    rights: EditUserRightsSchema | Unset = UNSET
    settings: EditUserSettingsSchema | Unset = UNSET
