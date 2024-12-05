

from asyncio import Server
from turtle import update
from typing import Optional, Sequence
import uuid

from sqlalchemy import select

from database.models.panel_server import PanelServer
from database.repositories.server_repository import ServerRepository
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from interface.proxy.models import VpnType


class PanelServerRepository(ServerRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self,
                     ip: str,
                     country_code: str,
                     display_name: str,
                     created_date: Optional[datetime] = None,
                     closing_date: Optional[datetime] = None,
                     is_available: bool = True,
                     panel_path: str = "",
                     login: str = "",
                     password: str = "",
                     vless_id: int = 0,
                     vless_reality_id: int = 0,
                     vmess_id: int = 0,
                     vless_port: int = 0,
                     vless_domain_short_id: str = "",
                     vless_reality_port: int = 0,
                     vless_reality_domain_short_id: str = "",
                     vless_reality_public_key: str = "",
                     vless_reality_private_key: str = "",
                     vmess_port: int = 0,
                     vmess_domain_short_id: str = ""
                     ) -> Optional[PanelServer]:
        panel_server = PanelServer(
            ip=ip,
            country_code=country_code,
            display_name=display_name,
            created_date=created_date,
            closing_date=closing_date,
            is_available=is_available,
            panel_path=panel_path,
            login=login,
            password=password,
            vless_id=vless_id,
            vless_reality_id=vless_reality_id,
            vmess_id=vmess_id,
            vless_port=vless_port,
            vless_domain_short_id=vless_domain_short_id,
            vless_reality_port=vless_reality_port,
            vless_reality_domain_short_id=vless_reality_domain_short_id,
            vless_reality_public_key=vless_reality_public_key,
            vless_reality_private_key=vless_reality_private_key,
            vmess_port=vmess_port,
            vmess_domain_short_id=vmess_domain_short_id
        )
        self.session.add(panel_server)
        await self.session.flush()

    async def get_by_id(self, id: uuid.UUID) -> Optional[PanelServer]:
        stmt = select(PanelServer).where(PanelServer.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_all(self) -> Sequence[PanelServer]:
        stmt = select(PanelServer)
        return list((await self.session.scalars(stmt)).all())

    async def update_vpn(self,
                         server: PanelServer,
                         id: int,
                         port: int,
                         domain_short_id: str,
                         vpn_type: VpnType,
                         public_key: str = "",
                         private_key: str = ""
                         ) -> None:
        setattr(server, vpn_type.value, id)
        setattr(server, f"{vpn_type.value[:-3]}_port", port)
        setattr(server,
                f"{vpn_type.value[:-3]}_domain_short_id", domain_short_id)
        if vpn_type == VpnType.VLESS_REALITY:
            setattr(server, f"{vpn_type.value[:-3]}_public_key", public_key)
            setattr(server, f"{vpn_type.value[:-3]}_private_key", private_key)
        await self.session.flush()