
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from shared.database import (
    UNSET,
    Protocols,
    Server,
    ServerInbound,
    Unset
)


class ServerSchema(BaseModel):
    id: UUID
    ip: str
    secured: bool
    description: str
    country_code: str
    display_name: str

    starting_date: datetime
    closing_date: datetime

    panel_port: int
    panel_web_path: str
    panel_login: str
    panel_password: str

    @classmethod
    def from_db(
        cls,
        server: Server
    ) -> 'ServerSchema':
        return ServerSchema(
            id=server.id,
            description=server.description,
            display_name=server.display_name,
            ip=server.ip,
            secured=server.secured,
            country_code=server.country_code,
            starting_date=server.starting_date,
            closing_date=server.closing_date,
            panel_port=server.panel_port,
            panel_web_path=server.panel_web_path,
            panel_login=server.panel_login,
            panel_password=server.panel_password
        )


class EditServerSchema(BaseModel):
    ip: str | Unset = UNSET
    secured: bool | Unset = UNSET
    description: str | Unset = UNSET
    country_code: str | Unset = UNSET
    display_name: str | Unset = UNSET

    starting_date: datetime | Unset = UNSET
    closing_date: datetime | Unset = UNSET

    panel_port: int | Unset = UNSET
    panel_web_path: str | Unset = UNSET
    panel_login: str | Unset = UNSET
    panel_password: str | Unset = UNSET


class CreateServerSchema(BaseModel):
    ip: str
    secured: bool
    description: str
    panel_port: int
    panel_web_path: str
    country_code: str
    display_name: str
    panel_login: str
    panel_password: str
    starting_date: datetime
    closing_date: datetime


class ServerInboundSchema(BaseModel):
    id: UUID
    inbound_id: int
    template: str
    protocol: str
    name: str
    description: str
    is_available: bool

    @classmethod
    def from_db(
        cls,
        server_inbound: ServerInbound
    ) -> 'ServerInboundSchema':
        return ServerInboundSchema(
            id=server_inbound.id,
            inbound_id=server_inbound.inbound_id,
            template=server_inbound.template,
            protocol=server_inbound.protocol,
            name=server_inbound.name,
            description=server_inbound.description,
            is_available=server_inbound.is_available
        )


class EditServerInboundSchema(BaseModel):
    inbound_id: int | Unset = UNSET
    template: str | Unset = UNSET
    protocol: str | Unset = UNSET
    name: str | Unset = UNSET
    description: str | Unset = UNSET
    is_available: bool | Unset = UNSET


class CreateServerInboundSchema(BaseModel):
    inbound_id: int
    template: str
    protocol: str
    name: str
    description: str
    is_available: bool

class ProtocolsSchema(BaseModel):
    data: dict[Protocols, str]
