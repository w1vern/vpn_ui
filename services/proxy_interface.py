


import abc
from typing import Optional

from httpx import Proxy

from database.models.user import User
from services.proxy_models import ProxyInbound, ProxyType, VpnInbound, VpnType


class ProxyInterface(abc.ABC):

    @abc.abstractmethod
    async def create_proxy(self, user: User, login: str, password: str, proxy_type: ProxyType) -> Optional[ProxyInbound]: ...
    
    @abc.abstractmethod
    async def create_vpn(self, user: User, vpn_type: VpnType) -> Optional[VpnInbound]: ...



