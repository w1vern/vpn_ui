

from sqlalchemy import ForeignKey
from database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from database.models.server import Server
from database.models.user import User
from interface.proxy.models import AccessConfig, AccessType, VpnConfig


class ServerUserInbound(Base):
    __tablename__ = "user_server_inbounds"

    server_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("servers.id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), primary_key=True)

    config: Mapped[AccessConfig] = mapped_column()
    type: Mapped[AccessType] = mapped_column()

    server: Mapped[Server] = relationship(
        lazy="selectin", foreign_keys=[server_id])
    user: Mapped[User] = relationship(lazy="selectin", foreign_keys=[user_id])
