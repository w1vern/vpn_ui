


import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base
from database.models.server import Server


class PanelServer(Server):
    __tablename__ = 'panel_servers'

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey('servers.id'), primary_key=True)

    panel_path: Mapped[str] = mapped_column()
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    vless_id: Mapped[int] = mapped_column()
    vless_port: Mapped[int] = mapped_column()
    vless_domain_short_id: Mapped[str] = mapped_column()
    vless_reality_id: Mapped[int] = mapped_column()
    vless_reality_port: Mapped[int] = mapped_column()
    vless_reality_domain_short_id: Mapped[str] = mapped_column()
    vless_reality_public_key: Mapped[str] = mapped_column()
    vless_reality_private_key: Mapped[str] = mapped_column()
    vmess_id: Mapped[int] = mapped_column()
    vmess_port: Mapped[int] = mapped_column()
    vmess_domain_short_id: Mapped[str] = mapped_column()

    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }

    @property
    def connection_string(self):
        return 'https://' + self.ip + '/' + self.panel_path + ''