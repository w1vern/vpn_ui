

import uuid
from datetime import datetime

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
    ip: str | None
    country_code: str | None
    is_available: bool | None
    display_name: str | None
    created_date: str | None
    closing_date: str | None

    panel_path: str | None
    login: str | None
    password: str | None

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

