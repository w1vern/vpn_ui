
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from shared.proxy_interface import (
    VpnType,
)

from ..models import (
    PanelServer,
    Server,
)
from .base import (
    BaseRepository,
)


class PanelServerRepository(BaseRepository[PanelServer]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, PanelServer)

    async def create(self,
                     server: Server,
                     panel_port: int,
                     port_generator_port: int,
                     web_path: str,
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
        return await self.__create(
            id=server.id,
            panel_port=panel_port,
            port_generator_port=port_generator_port,
            web_path=web_path,
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

    async def set_panel_port(self,
                             server: PanelServer,
                             panel_port: int
                             ) -> None:
        server.panel_port = panel_port
        await self.session.flush()

    async def set_port_generator_port(self,
                                      server: PanelServer,
                                      port_generator_port: int
                                      ) -> None:
        server.port_generator_port = port_generator_port
        await self.session.flush()

    async def set_web_path(self,
                           server: PanelServer,
                           web_path: str
                           ) -> None:
        server.web_path = web_path
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
