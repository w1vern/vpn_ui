

from sqlalchemy import ForeignKey
from database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from database.models.server import Server
from database.models.user import User
from interface.proxy.models import AccessConfig, AccessConfigFactory, AccessType, VpnConfig


class ServerUserInbound(Base):
    __tablename__ = "server_user_inbounds"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    server_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("servers.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"))

    config_str: Mapped[str] = mapped_column()

    server: Mapped[Server] = relationship(
        lazy="selectin", foreign_keys=[server_id])
    user: Mapped[User] = relationship(lazy="selectin", foreign_keys=[user_id])

    @property
    def config(self):
        return AccessConfigFactory.from_string(self.config_str)
    
    @property
    def access_type(self):
        return self.config.access_type
