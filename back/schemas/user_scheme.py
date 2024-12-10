

from datetime import datetime
from operator import is_
from typing import Optional
import uuid
from pydantic import BaseModel


class UserScheme(BaseModel):
    id: uuid.UUID
    telegram_id: str
    telegram_username: str
    balance: float
    created_date: str
    is_server_editor: bool
    is_transaction_editor: bool
    is_active_period_editor: bool
    is_tariff_editor: bool
    is_member_rights_editor: bool
    is_admin_rights_editor: bool
    is_control_panel_user: bool
    is_active: bool
    verified: bool
    auto_pay: bool

class EditUserScheme(BaseModel):
    id: uuid.UUID

    created_date: Optional[str]
    is_server_editor: Optional[bool]
    is_transaction_editor: Optional[bool]
    is_active_period_editor: Optional[bool]
    is_tariff_editor: Optional[bool]
    is_member_rights_editor: Optional[bool]
    is_admin_rights_editor: Optional[bool]
    is_control_panel_user: Optional[bool]
    is_active: Optional[bool]
    verified: Optional[bool]
    auto_pay: Optional[bool]
    