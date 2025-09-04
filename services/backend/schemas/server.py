

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from shared.database import PanelServer


class ServerSchema(BaseModel):
    id: UUID
    ip: str
    description: str
    country_code: str
    is_available: bool
    display_name: str
    starting_date: datetime
    closing_date: datetime

    panel_path: str
    login: str
    password: str

    @classmethod
    def from_db(cls,
                server: PanelServer
                ) -> 'ServerSchema':
        return ServerSchema(
            id=server.id,
            description=server.server.description,
            display_name=server.server.display_name,
            ip=server.server.ip,
            country_code=server.server.country_code,
            is_available=server.server.is_available,
            starting_date=server.server.starting_date,
            closing_date=server.server.closing_date,
            panel_path=server.panel_path,
            login=server.login,
            password=server.password
        )


class ServerToEditSchema(BaseModel):
    ip: str | None = None
    description: str | None = None
    country_code: str | None = None
    is_available: bool | None = None
    display_name: str | None = None
    starting_date: datetime | None = None
    closing_date: datetime | None = None

    panel_path: str | None = None
    login: str | None = None
    password: str | None = None


class CreateServerSchema(BaseModel):
    ip: str
    description: str
    panel_path: str
    country_code: str
    is_available: bool
    display_name: str
    login: str
    password: str
    starting_date: datetime
    closing_date: datetime
