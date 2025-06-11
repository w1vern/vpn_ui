

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from shared.database import User


class UserSettingsSchema(BaseModel):
    auto_pay: bool
    is_active: bool
    get_traffic_notifications: bool

    model_config = ConfigDict(from_attributes=True)


class UserRightsSchema(BaseModel):
    is_server_editor: bool
    is_transaction_editor: bool
    is_active_period_editor: bool
    is_tariff_editor: bool
    is_member_rights_editor: bool
    is_admin_rights_editor: bool
    is_control_panel_user: bool
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    id: uuid.UUID
    telegram_id: int
    telegram_username: str
    balance: float
    created_date: str
    rights: UserRightsSchema
    settings: UserSettingsSchema

    model_config = ConfigDict(
        json_encoders={
            uuid.UUID: lambda v: str(v),
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
            telegram_id=user.telegram_id,
            telegram_username=user.telegram_username,
            balance=user.balance,
            created_date=user.created_date.isoformat(),
            rights=rights,
            settings=settings
        )


class EditUserSettingsSchema(BaseModel):
    auto_pay: bool | None
    is_active: bool | None
    get_traffic_notifications: bool | None


class EditUserRightsSchema(BaseModel):
    is_server_editor: bool | None
    is_transaction_editor: bool | None
    is_active_period_editor: bool | None
    is_tariff_editor: bool | None
    is_member_rights_editor: bool | None
    is_admin_rights_editor: bool | None
    is_control_panel_user: bool | None
    is_verified: bool | None


class EditUserSchema(BaseModel):
    telegram_id: int | None
    created_date: str | None
    rights: EditUserRightsSchema | None
    settings: EditUserSettingsSchema | None
