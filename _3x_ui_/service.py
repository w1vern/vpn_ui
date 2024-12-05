

import random

import secrets
import string
from typing import Optional
import uuid
from httpx import Proxy
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.panel_server import PanelServer
from database.repositories.panel_server_repository import PanelServerRepository
from interface.proxy.interface import ProxyInterface
from interface.proxy.models import AccessConfig, AccessType, NoneSecurity, ProxyConfig, ProxyType, RealityOptions, VpnConfig, VpnType, Security
from _3x_ui_.repository import PanelRepository
from _3x_ui_.session_manager import ServerSession
from database.models.user import User
from database.repositories.server_repository import ServerRepository
from database.repositories.server_user_inbound_repository import ServerUserInboundRepository
from database.repositories.user_repository import UserRepository
from database.models.server import Server


def generate_sub_id(length: int = 16) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_short_ids(count: int = 1) -> list[str]:
    res = []
    for i in range(count):
        length = random.randint(16, 16)
        res.append(
            hex(random.randint(0b1 << 4 * (length-1), 0b1 << 4 * length))[2:])
    return res


def generate_email(user: User, vpn_type: VpnType) -> str:
    return f"{user.telegram_username}-{vpn_type.value[:-3]}-{uuid.uuid4()}"


def generate_vpn_remark(vpn_type: VpnType) -> str:
    return f"{vpn_type.value[:-3]}"


def generate_proxy_remark(server: PanelServer, user: User, proxy_type: ProxyType) -> str:
    return f"{proxy_type.value[:-3]}-{user.telegram_username}"


def generate_user_remark(server: PanelServer, user: User, vpn_type: VpnType) -> str:
    return f"{server.country_code}-{server.display_name}-{user.telegram_username}-{vpn_type.value[:-3]}"


def generate_key(length: int = 43) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits + "-_", k=length))


class Service(ProxyInterface):
    def __init__(self, db_session: AsyncSession, server_session: ServerSession) -> None:
        self.db_session = db_session
        self.server_session = server_session
        self.pr = PanelRepository(server_session)
        self.psr = PanelServerRepository(db_session)
        self.suir = ServerUserInboundRepository(db_session)

    async def get_config(self,
                         user: User,
                         access_type: AccessType = AccessType.HTTP,
                         create_if_not_exists: bool = True,
                         login: str = "",
                         password: str = ""
                         ) -> Optional[AccessConfig]:
        inbounds = await self.suir.get_by_server_and_user(self.server_session.server, user)
        for inbound in inbounds:
            if inbound.access_type == access_type:
                if await self.config_is_valid(user, inbound.config) is True:
                    return inbound.config
                break
        if create_if_not_exists is False:
            return None
        if access_type in ProxyType:
            response = await self.__create_proxy(user, login, password, ProxyType(access_type))
        elif access_type in VpnType:
            response = await self.__create_vpn(user, VpnType(access_type))
        else:
            return None
        if response is None:
            return None
        await self.suir.create(self.server_session.server, user, response)
        return response

    async def config_is_valid(self, user: User, config: AccessConfig) -> bool:
        return True

    async def __create_proxy(self,
                             user: User,
                             login: str = "",
                             password: str = "",
                             proxy_type: ProxyType = ProxyType.HTTP,
                             ) -> Optional[ProxyConfig]:
        if login == "":
            login = secrets.token_urlsafe(8)
        if password == "":
            password = secrets.token_urlsafe(8)
        response = await self.pr.create_proxy(remark=generate_proxy_remark(self.server_session.server, user, proxy_type), login=login, password=password, port=await self.pr.get_free_port(), user=user, proxy_type=proxy_type)
        if response['success'] is False:
            return None
        return ProxyConfig(access_type=AccessType(proxy_type.value),
                           ip=self.server_session.server.ip,
                           port=response['obj']['port'],
                           login=response['obj']['settings']['accounts'][0]['user'],
                           password=response['obj']['settings']['accounts'][0]['pass'])

    async def __create_vpn(self,
                           user: User,
                           vpn_type: VpnType = VpnType.VLESS_REALITY,
                           ) -> Optional[VpnConfig]:
        uuid4 = uuid.uuid4()
        sub_id = generate_sub_id()
        email = generate_email(user, vpn_type)
        protocol = vpn_type.value[:-3]
        if vpn_type == VpnType.VLESS_REALITY:
            protocol = "vless"
        if getattr(self.server_session.server, vpn_type.value) == 0:
            remark = generate_vpn_remark(vpn_type)
            short_ids = generate_short_ids()
            port = await self.pr.get_free_port()
            public_key = generate_key()
            private_key = generate_key()
            response = await self.pr.create_vpn(remark=remark,
                                                protocol=protocol,
                                                user=user, sub_id=sub_id,
                                                short_ids=short_ids,
                                                vpn_type=vpn_type,
                                                uuid4=uuid4,
                                                port=port,
                                                email=email,
                                                public_key=public_key,
                                                private_key=private_key)
            if response['success'] is False:
                return None
            await self.psr.update_vpn(server=self.server_session.server,
                                      id=response['obj']['id'],
                                      port=port,
                                      domain_short_id=short_ids[0],
                                      vpn_type=vpn_type,
                                      public_key=public_key,
                                      private_key=private_key)
        else:
            response = await self.pr.create_vpn_user(user=user, vpn_type=vpn_type, uuid4=uuid4, sub_id=sub_id, email=email)
            if response['success'] is False:
                return None
        security = NoneSecurity()
        if vpn_type == VpnType.VLESS_REALITY:
            security = RealityOptions(public_key=self.server_session.server.vless_reality_public_key,
                                      fp="random",
                                      server_name_indication="yahoo.com",
                                      sid=getattr(self.server_session.server,
                                                  f"{vpn_type.value[:-3]}_domain_short_id"),
                                      spx="/", )
        return VpnConfig(access_type=AccessType(vpn_type.value),
                         uuid=str(uuid4),
                         ip=self.server_session.server.ip,
                         port=getattr(self.server_session.server,
                         f"{vpn_type.value[:-3]}_port"),
                         protocol=protocol,
                         path="",
                         header_type="http",
                         security=security,
                         remark=generate_user_remark(self.server_session.server, user, vpn_type))

    async def toggle_active(self,
                            user: User,
                            access_type: Optional[AccessType] = None,
                            delete: bool = False
                            ) -> None:
        if access_type in VpnType:
            return
        elif access_type in ProxyType:
            return
        else:
            return

    async def get_configs(self, user: User) -> list[AccessConfig]:
        suis = await self.suir.get_by_server_and_user(self.server_session.server, user)
        configs = []
        for sui in suis:
            if not self.config_is_valid(user, sui.config):
                del (suis[suis.index(sui)])
            else:
                configs.append(sui.config)
        return configs

    async def get_traffic(self, user: User) -> int:
        return 0

    async def reset_traffic(self, user: User) -> None:
        return
