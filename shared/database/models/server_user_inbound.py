
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from shared.proxy_interface import (
    AccessConfig,
    AccessConfigFactory,
    AccessType,
)

from .base import Base
from .server import Server
from .user import User


class ServerUserInbound(Base):
    __tablename__ = "server_user_inbounds"

    server_id: Mapped[UUID] = mapped_column(
        ForeignKey("servers.id"))
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"))

    config_str: Mapped[str] = mapped_column()

    server: Mapped[Server] = relationship(
        lazy="selectin", foreign_keys=[server_id])
    user: Mapped[User] = relationship(lazy="selectin", foreign_keys=[user_id])

    @property
    def config(self) -> AccessConfig:
        return AccessConfigFactory.from_string(self.config_str)

    @property
    def access_type(self) -> AccessType:
        return self.config.access_type
