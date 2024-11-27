


from sqlalchemy import ForeignKey
from database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from datetime import datetime

from database.models.server import Server


class ServerPanel(Server):
    __tablename__ = 'servers_panel'

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey('servers.id'), primary_key=True)

    panel_path: Mapped[str] = mapped_column()
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    vless_id: Mapped[int] = mapped_column()
    vless_reality_id: Mapped[int] = mapped_column()
    vmess_id: Mapped[int] = mapped_column()

    @property
    def connection_string(self):
        return 'https://' + self.ip + '/' + self.panel_path + ''