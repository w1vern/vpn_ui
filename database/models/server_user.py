

from sqlalchemy import ForeignKey
from database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from database.models.server import Server
from database.models.user import User


class ServerUser(Base):
    __tablename__ = "servers_and_users"

    server_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("servers.id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), primary_key=True)

    vless_id: Mapped[uuid.UUID] = mapped_column()
    vless_reality_id: Mapped[uuid.UUID] = mapped_column()
    vmess_id: Mapped[uuid.UUID] = mapped_column()
    http_id: Mapped[int] = mapped_column()
    socks_id: Mapped[int] = mapped_column()

    server: Mapped[Server] = relationship(
        lazy="selectin", foreign_keys=[server_id])
    user: Mapped[User] = relationship(lazy="selectin", foreign_keys=[user_id])
