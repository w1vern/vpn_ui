

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ServerToCreate(BaseModel):
    ip: str
    panel_path: str
    country_code: str
    is_available: Optional[bool]
    display_name: str
    login: str
    password: str
    created_date: Optional[datetime]
    closing_date: Optional[datetime]

