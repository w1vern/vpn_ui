
from math import log
import random
from re import sub
import secrets
import string
from typing import Optional
from urllib import response
from sqlalchemy.ext.asyncio import AsyncSession

from services.proxy_interface import ProxyInterface
from services.proxy_models import ProxyInbound, ProxyType, VpnInbound, VpnType
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


class Service(ProxyInterface):
    def __init__(self, db_session: AsyncSession, server_session: ServerSession) -> None:
        self.db_session = db_session
        self.server_session = server_session
        self.pr = PanelRepository(server_session)
        self.ur = UserRepository(db_session)
        self.sr = ServerRepository(db_session)
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
        response = await self.pr.create_proxy(login=login, password=password, port=await self.pr.get_free_port(), user=user, proxy_type=proxy_type)
        if response['success'] is False:
            return None
        connections = await self.sur.get_by_id(self.server_session.server.id, user.id)
        params = dict()
        params[proxy_type.value] = response['obj']['id']
        if connections is None:
            connections = self.sur.create(
                self.server_session.server, user, **params)
        else:
            params[ProxyType.HTTP.value] = connections.http_id
            params[ProxyType.SOCKS.value] = connections.socks_id
            params[proxy_type.value] = response['obj']['id']
            await self.sur.update_ids(self.server_session.server, user, **params, vless_id=connections.vless_id, vless_reality_id=connections.vless_reality_id, vmess_id=connections.vmess_id)
        return ProxyInbound(self.server_session.server.ip, response['obj']['port'],
                            response['obj']['settings']['accounts'][0]['user'],
                            response['obj']['settings']['accounts'][0]['pass'])

    async def create_vpn(self, server: Server, user: User, vpn_type: VpnType) -> Optional[VpnInbound]:
        protocol = vpn_type.value[:-3]
        if vpn_type == VpnType.VLESS_REALITY:
            protocol = "vless"
        sub_id = generate_sub_id()
        short_ids = generate_short_ids()
        
