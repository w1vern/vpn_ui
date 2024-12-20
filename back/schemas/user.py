

import uuid
from typing import Optional
from venv import create

from pydantic import BaseModel


class UserSettingsScheme(BaseModel):
    auto_pay: bool
    is_active: bool
    get_traffic_notifications: bool


class UserRightsScheme(BaseModel):
    is_server_editor: bool
    is_transaction_editor: bool
    is_active_period_editor: bool
    is_tariff_editor: bool
    is_member_rights_editor: bool
    is_admin_rights_editor: bool
    is_control_panel_user: bool
    is_verified: bool


class UserScheme(BaseModel):
    id: uuid.UUID
    telegram_id: str
    telegram_username: str
    balance: float
    created_date: str
    rights: UserRightsScheme
    settings: UserSettingsScheme


class EditUserSettingsScheme(BaseModel):
    auto_pay: Optional[bool]
    is_active: Optional[bool]
    get_traffic_notifications: Optional[bool]


class EditUserRightsScheme(BaseModel):
    is_server_editor: Optional[bool]
    is_transaction_editor: Optional[bool]
    is_active_period_editor: Optional[bool]
    is_tariff_editor: Optional[bool]
    is_member_rights_editor: Optional[bool]
    is_admin_rights_editor: Optional[bool]
    is_control_panel_user: Optional[bool]
    is_verified: Optional[bool]


class EditUserScheme(BaseModel):
    id: uuid.UUID
    telegram_id: Optional[str]
    created_date: Optional[str]
    rights: Optional[EditUserRightsScheme]
    settings: Optional[EditUserSettingsScheme]
