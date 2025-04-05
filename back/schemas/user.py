

import uuid
from typing import Optional
from venv import create

from pydantic import BaseModel

from database.models.user import User


class UserSettingsSchema(BaseModel):
    auto_pay: bool
    is_active: bool
    get_traffic_notifications: bool

    class Config:
        from_attributes = True


class UserRightsSchema(BaseModel):
    is_server_editor: bool
    is_transaction_editor: bool
    is_active_period_editor: bool
    is_tariff_editor: bool
    is_member_rights_editor: bool
    is_admin_rights_editor: bool
    is_control_panel_user: bool
    is_verified: bool

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: uuid.UUID
    telegram_id: str
    telegram_username: str
    balance: float
    created_date: str
    rights: UserRightsSchema
    settings: UserSettingsSchema

    class Config:
        from_attributes = True

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
    auto_pay: Optional[bool]
    is_active: Optional[bool]
    get_traffic_notifications: Optional[bool]


class EditUserRightsSchema(BaseModel):
    is_server_editor: Optional[bool]
    is_transaction_editor: Optional[bool]
    is_active_period_editor: Optional[bool]
    is_tariff_editor: Optional[bool]
    is_member_rights_editor: Optional[bool]
    is_admin_rights_editor: Optional[bool]
    is_control_panel_user: Optional[bool]
    is_verified: Optional[bool]


class EditUserSchema(BaseModel):
    id: uuid.UUID
    telegram_id: Optional[str]
    created_date: Optional[str]
    rights: Optional[EditUserRightsSchema]
    settings: Optional[EditUserSettingsSchema]
