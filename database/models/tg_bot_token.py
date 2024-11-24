

import token
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base
from database.models.server import Server


class TgBotToken(Base):
    __tablename__ = 'tg_bot_tokens'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    token: Mapped[str] = mapped_column()
    server_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('servers.id'))

    server: Mapped[Server] = relationship(lazy='selectin', foreign_keys=[server_id])
