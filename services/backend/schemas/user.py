

from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
)

from shared.database import User

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
    balance: float
    created_date: str
    rights: UserRightsSchema
    settings: UserSettingsSchema

    tariff: TariffSchema

    model_config = ConfigDict(
        json_encoders={
            UUID: lambda v: str(v),
            datetime: lambda v: v.isoformat()
        },
        from_attributes=True
    )

    @classmethod
    def from_db(cls, user: User) -> "UserSchema":
        settings = UserSettingsSchema.model_validate(user)
        rights = UserRightsSchema.model_validate(user)
        return UserSchema(
            id=user.id,
            tariff=TariffSchema.from_db(user.tariff),
            telegram_id=user.telegram_id,
            telegram_username=user.telegram_username,
            balance=user.balance,
            created_date=user.created_date.isoformat(),
            rights=rights,
            settings=settings
        )


class EditUserSettingsSchema(BaseModel):
    auto_pay: bool | None = None
    is_active: bool | None = None
    get_traffic_notifications: bool | None = None


class EditUserRightsSchema(BaseModel):
    is_server_editor: bool | None = None
    is_user_editor: bool | None = None
    is_transaction_editor: bool | None = None
    is_active_period_editor: bool | None = None
    is_tariff_editor: bool | None = None
    is_member_rights_editor: bool | None = None
    is_admin_rights_editor: bool | None = None
    is_control_panel_user: bool | None = None
    is_verified: bool | None = None


class EditUserSchema(BaseModel):
    telegram_id: int | None = None
    tariff_id: UUID | None = None
    rights: EditUserRightsSchema | None = None
    settings: EditUserSettingsSchema | None = None
