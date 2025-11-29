
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

    panel_port: int
    port_generator_port: int
    web_path: str
    login: str
    password: str

    vless_reality_id: int | None
    vless_reality_port: int | None
    vless_reality_domain_short_id: str | None
    vless_reality_public_key: str | None
    vless_reality_private_key: str | None

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
            panel_port=server.panel_port,
            port_generator_port=server.port_generator_port,
            web_path=server.web_path,
            login=server.login,
            password=server.password,
            vless_reality_id=server.vless_reality_id,
            vless_reality_port=server.vless_reality_port,
            vless_reality_domain_short_id=server.vless_reality_domain_short_id,
            vless_reality_public_key=server.vless_reality_public_key,
            vless_reality_private_key=server.vless_reality_private_key
        )


class ServerToEditSchema(BaseModel):
    ip: str | None = None
    description: str | None = None
    country_code: str | None = None
    is_available: bool | None = None
    display_name: str | None = None
    starting_date: datetime | None = None
    closing_date: datetime | None = None

    panel_port: int | None = None
    port_generator_port: int | None = None
    web_path: str | None = None
    login: str | None = None
    password: str | None = None

    vless_reality_id: int | None = None
    vless_reality_port: int | None = None
    vless_reality_domain_short_id: str | None = None
    vless_reality_public_key: str | None = None
    vless_reality_private_key: str | None = None


class CreateServerSchema(BaseModel):
    ip: str
    description: str
    panel_port: int
    port_generator_port: int
    web_path: str
    country_code: str
    is_available: bool
    display_name: str
    login: str
    password: str
    starting_date: datetime
    closing_date: datetime

    vless_reality_id: int
    vless_reality_port: int
    vless_reality_domain_short_id: str
    vless_reality_public_key: str
    vless_reality_private_key: str
