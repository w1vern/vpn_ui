
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models import PanelServer, Server
from interfaces.proxy.models import VpnType

from .base_repository import BaseRepository


class PanelServerRepository(BaseRepository[PanelServer]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, PanelServer)

    async def create(self,
                     server: Server,
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
                     ) -> PanelServer:
        return await self.universal_create(
            id=server.id,
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

    async def set_login(self,
                        server: PanelServer,
                        login: str
                        ) -> None:
        server.login = login
        await self.session.flush()

    async def set_password(self,
                           server: PanelServer,
                           password: str
                           ) -> None:
        server.password = password
        await self.session.flush()

    async def set_panel_path(self,
                             server: PanelServer,
                             panel_path: str
                             ) -> None:
        server.panel_path = panel_path
        await self.session.flush()

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
