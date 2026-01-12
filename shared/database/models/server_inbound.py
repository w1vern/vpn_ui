
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .server import Server


class ServerInbound(BaseModel):
    __tablename__ = "server_inbounds"

    inbound_id: Mapped[int]
    template: Mapped[str]
    protocol: Mapped[str]
    server_id: Mapped[UUID] = mapped_column(ForeignKey("servers.id"))
    name: Mapped[str]
    description: Mapped[str]
    is_available: Mapped[bool]

    server: Mapped[Server] = relationship(
        lazy="selectin", foreign_keys=[server_id])
