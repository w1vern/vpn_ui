

from asyncio import Server
from turtle import update
from typing import Optional, Sequence
import uuid

from sqlalchemy import select

from database.models.panel_server import PanelServer
from database.repositories.server_repository import ServerRepository
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession


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
                     vmess_id: int = 0
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
            vmess_id=vmess_id
        )
        self.session.add(panel_server)
        await self.session.flush()

    async def get_by_id(self, id: uuid.UUID) -> Optional[PanelServer]:
        stmt = select(PanelServer).where(PanelServer.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_all(self) -> Sequence[PanelServer]:
        stmt = select(PanelServer)
        return list((await self.session.scalars(stmt)).all())

    async def update_vpn_ids(self,
                             server: PanelServer,
                             vless_id: int,
                             vless_reality_id: int,
                             vmess_id: int
                             ) -> None:
        server.vless_id = vless_id
        server.vless_reality_id = vless_reality_id
        server.vmess_id = vmess_id
        await self.session.flush()
