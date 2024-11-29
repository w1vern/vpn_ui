
from math import e, log
import random
from re import sub
import re
import secrets
import string
from typing import Optional
from urllib import response
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.panel_server import PanelServer
from database.repositories.panel_server_repository import PanelServerRepository
from services.proxy_interface import ProxyInterface
from services.proxy_models import ProxyInbound, ProxyType, RealityOptions, VpnInbound, VpnType, Security
from _3x_ui_.repository import PanelRepository
from _3x_ui_.session_manager import ServerSession
from database.models.user import User
from database.repositories.server_repository import ServerRepository
from database.repositories.server_user_repository import ServerUserRepository
from database.repositories.user_repository import UserRepository
from database.models.server import Server


def generate_sub_id(length: int = 16) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_short_ids(count: int = 8) -> list[str]:
    res = []
    for i in range(count):
        length = random.randint(2, 16)
        res.append(
            hex(random.randint(0b1 << 4 * (length-1), 0b1 << 4 * length))[2:])
    return res


def generate_email(server: PanelServer, user: User, vpn_type: VpnType) -> str:
    return f"{user.telegram_username}-{vpn_type.value[:-3]}-{uuid.uuid4()}"


def generate_vpn_remark(server: PanelServer, vpn_type: VpnType) -> str:
    return f"{vpn_type.value[:-3]}"


def generate_proxy_remark(server: PanelServer, user: User, proxy_type: ProxyType) -> str:
    return f"{proxy_type.value[:-3]}-{user.telegram_username}"


class Service(ProxyInterface):
    def __init__(self, db_session: AsyncSession, server_session: ServerSession) -> None:
        self.db_session = db_session
        self.server_session = server_session
        self.pr = PanelRepository(server_session)
        self.ur = UserRepository(db_session)
        self.psr = PanelServerRepository(db_session)
        self.sur = ServerUserRepository(db_session)

    async def create_proxy(self,
                           user: User,
                           login: str = "",
                           password: str = "",
                           proxy_type: ProxyType = ProxyType.HTTP) -> Optional[ProxyInbound]:
        if login == "":
            login = secrets.token_urlsafe(8)
        if password == "":
            password = secrets.token_urlsafe(8)
        response = await self.pr.create_proxy(remark=generate_proxy_remark(self.server_session.server, user, proxy_type), login=login, password=password, port=await self.pr.get_free_port(), user=user, proxy_type=proxy_type)
        if response['success'] is False:
            return None
        connections = await self.sur.get_by_id(self.server_session.server.id, user.id)
        params = dict()
        params[proxy_type.value] = response['obj']['id']
        if connections is None:
            connections = await self.sur.create(
                self.server_session.server, user, **params)
        else:
            params[ProxyType.HTTP.value] = connections.http_id
            params[ProxyType.SOCKS.value] = connections.socks_id
            params[proxy_type.value] = response['obj']['id']
            await self.sur.update_ids(self.server_session.server, user, **params, vless_id=connections.vless_id, vless_reality_id=connections.vless_reality_id, vmess_id=connections.vmess_id)
        return ProxyInbound(self.server_session.server.ip, response['obj']['port'],
                            response['obj']['settings']['accounts'][0]['user'],
                            response['obj']['settings']['accounts'][0]['pass'])

    async def create_vpn(self, user: User, vpn_type: VpnType) -> Optional[VpnInbound]:
        uuid4 = uuid.uuid4()
        sub_id = generate_sub_id()
        email = generate_email(self.server_session.server, user, vpn_type)
        protocol = vpn_type.value[:-3]
        remark = generate_vpn_remark(self.server_session.server, vpn_type)
        server_exists = True
        if vpn_type == VpnType.VLESS_REALITY:
            protocol = "vless"
        if getattr(self.server_session.server, vpn_type.value) == 0:
            server_exists = False
            short_ids = generate_short_ids()
            port = await self.pr.get_free_port()
            response = await self.pr.create_vpn(remark=remark, protocol=protocol, user=user, sub_id=sub_id, short_ids=short_ids, vpn_type=vpn_type, uuid4=uuid4, port=port, email=email)
            if response['success'] is False:
                return None
            params = dict()
            params[VpnType.VLESS.value] = self.server_session.server.vless_id
            params[VpnType.VLESS_REALITY.value] = self.server_session.server.vless_reality_id
            params[VpnType.VMESS.value] = self.server_session.server.vmess_id
            params[vpn_type.value] = response['obj']['id']
            await self.psr.update_vpn_ids(self.server_session.server, **params)
        else:
            response = await self.pr.create_vpn_user(user=user, vpn_type=vpn_type, uuid4=uuid4, sub_id=sub_id, email=email)
            if response['success'] is False:
                return None
        connections = await self.sur.get_by_id(self.server_session.server.id, user.id)
        if connections is None:
            connections = await self.sur.create(self.server_session.server, user)
            if connections is None:
                return None
        params = dict()
        params[VpnType.VLESS.value] = connections.vless_id
        params[VpnType.VLESS_REALITY.value] = connections.vless_reality_id
        params[VpnType.VMESS.value] = connections.vmess_id
        params[ProxyType.HTTP.value] = connections.http_id
        params[ProxyType.SOCKS.value] = connections.socks_id
        params[vpn_type.value] = uuid4
        await self.sur.update_ids(self.server_session.server, user, **params)
        security = Security()
        if vpn_type == VpnType.VLESS_REALITY:
            if server_exists is False:
                domain_short_id = sub_id[0]
            else:
                list = await self.server_session.get_dict(path='list')
                id = self.server_session.server.id
                for connection in list['obj']:
                    if connection['id'] == id:
                        port = connection['port']
                        domain_short_id = connection['streamSettings']['realitySettings']['shortIds'][0]
                        break
            security = RealityOptions(public_key="",
                                      fp="random",
                                      server_name_indication="yahoo.com",
                                      sid=domain_short_id,  # type: ignore
                                      spx="/", )
        return VpnInbound(uuid=str(uuid4),
                          ip=self.server_session.server.ip,
                          port=port,  # type: ignore
                          protocol=protocol,
                          path="",
                          header_type="http",
                          security=security,
                          remark=remark + '-' + email)
