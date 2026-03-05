
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

from shared.database import (
    UNSET,
    LanguageCodes,
    Unset,
    User,
    UserRights,
    UserSettings
)

from .tariff import TariffSchema


class UserSettingsSchema(BaseModel):
    auto_pay: bool
    is_active: bool
    get_traffic_notifications: bool
    language_code: LanguageCodes

    @classmethod
    def from_db(cls, settings: UserSettings) -> 'UserSettingsSchema':
        return cls(
            auto_pay=settings.auto_pay,
            is_active=settings.is_active,
            get_traffic_notifications=settings.get_traffic_notifications,
            language_code=LanguageCodes(settings.language_code)
        )


class UserRightsSchema(BaseModel):
    is_servers_editor: bool
    is_users_editor: bool
    is_transactions_editor: bool
    is_tariffs_editor: bool
    is_member_rights_editor: bool
    is_admin_rights_editor: bool
    is_control_panel_user: bool
    is_verified: bool

    @classmethod
    def from_db(cls, rights: UserRights) -> 'UserRightsSchema':
        return cls(
            is_servers_editor=rights.is_servers_editor,
            is_users_editor=rights.is_users_editor,
            is_transactions_editor=rights.is_transactions_editor,
            is_tariffs_editor=rights.is_tariffs_editor,
            is_member_rights_editor=rights.is_member_rights_editor,
            is_admin_rights_editor=rights.is_admin_rights_editor,
            is_control_panel_user=rights.is_control_panel_user,
            is_verified=rights.is_verified
        )


class UserSchema(BaseModel):
    id: UUID
    telegram_id: int
    telegram_username: str
    internal_id: str
    description: str
    balance: int
    created_date: datetime
    rights: UserRightsSchema
    settings: UserSettingsSchema

    tariff: TariffSchema

    @classmethod
    def from_db(cls, user: User) -> 'UserSchema':
        return cls(
            id=user.id,
            tariff=TariffSchema.from_db(user.tariff),
            telegram_id=user.telegram_id,
            telegram_username=user.telegram_username,
            internal_id=user.internal_id,
            balance=user.balance,
            created_date=user.created_date,
            description=user.description,
            rights=UserRightsSchema.from_db(user.rights),
            settings=UserSettingsSchema.from_db(user.settings)
        )


class EditUserSettingsSchema(BaseModel):
    auto_pay: bool | Unset = UNSET
    is_active: bool | Unset = UNSET
    get_traffic_notifications: bool | Unset = UNSET
    language_code: LanguageCodes | Unset = UNSET


class EditUserRightsSchema(BaseModel):
    is_servers_editor: bool | Unset = UNSET
    is_users_editor: bool | Unset = UNSET
    is_transactions_editor: bool | Unset = UNSET
    is_tariffs_editor: bool | Unset = UNSET
    is_member_rights_editor: bool | Unset = UNSET
    is_admin_rights_editor: bool | Unset = UNSET
    is_control_panel_user: bool | Unset = UNSET
    is_verified: bool | Unset = UNSET


class EditUserSchema(BaseModel):
    telegram_id: int | Unset = UNSET
    tariff_id: UUID | Unset = UNSET
    description: str | Unset = UNSET
    internal_id: str | Unset = UNSET
    rights: EditUserRightsSchema | Unset = UNSET
    settings: EditUserSettingsSchema | Unset = UNSET

    @field_validator('rights', mode='before')
    def parse_rights(cls, value: dict | EditUserRightsSchema | Unset) -> EditUserRightsSchema | Unset:
        if isinstance(value, dict):
            return EditUserRightsSchema.model_validate(value)
        return value

    @field_validator('settings', mode='before')
    def parse_settings(cls, value: dict | EditUserSettingsSchema | Unset) -> EditUserSettingsSchema | Unset:
        if isinstance(value, dict):
            return EditUserSettingsSchema.model_validate(value)
        return value
