

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ServerSchema(BaseModel):
    id: uuid.UUID
    ip: str
    country_code: str
    is_available: bool
    display_name: str
    created_date: str
    closing_date: str

    panel_path: str
    login: str
    password: str

class EditServerSchema(BaseModel):
    id: uuid.UUID
    ip: Optional[str]
    country_code: Optional[str]
    is_available: Optional[bool]
    display_name: Optional[str]
    created_date: Optional[str]
    closing_date: Optional[str]

    panel_path: Optional[str]
    login: Optional[str]
    password: Optional[str]

class ServerToCreateSchema(BaseModel):
    ip: str
    panel_path: str
    country_code: str
    is_available: bool
    display_name: str
    login: str
    password: str
    created_date: str
    closing_date: str

