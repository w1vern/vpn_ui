

from uuid import UUID

from pydantic import BaseModel

from shared.database import PanelServer


class ServerSchema(BaseModel):
    id: UUID
    ip: str
    country_code: str
    is_available: bool
    display_name: str
    starting_date: str
    closing_date: str

    panel_path: str
    login: str
    password: str

    @classmethod
    def from_db(cls,
                server: PanelServer
                ) -> 'ServerSchema':
        return ServerSchema(
            id=server.id,
            display_name=server.server.display_name,
            ip=server.server.ip,
            country_code=server.server.country_code,
            is_available=server.server.is_available,
            starting_date=server.server.starting_date.isoformat(),
            closing_date=server.server.closing_date.isoformat(),
            panel_path=server.panel_path,
            login=server.login,
            password=server.password
        )


class ServerToEditSchema(BaseModel):
    ip: str | None = None
    country_code: str | None = None
    is_available: bool | None = None
    display_name: str | None = None
    starting_date: str | None = None
    closing_date: str | None = None

    panel_path: str | None = None
    login: str | None = None
    password: str | None = None


class CreateServerSchema(BaseModel):
    ip: str
    panel_path: str
    country_code: str
    is_available: bool
    display_name: str
    login: str
    password: str
    starting_date: str
    closing_date: str
