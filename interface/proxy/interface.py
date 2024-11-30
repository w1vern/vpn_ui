

import abc
from typing import Optional

from database.models.user import User
from .models import ProxyConfig, ProxyType, VpnConfig, VpnType, AccessConfig, AccessType


class ProxyInterface(abc.ABC):

    @abc.abstractmethod
    async def get_proxy(self,
                        user: User,
                        login: str = "",
                        password: str = "",
                        proxy_type: ProxyType = ProxyType.HTTP,
                        create_if_not_exists: bool = True
                        ) -> Optional[ProxyConfig]: ...

    @abc.abstractmethod
    async def get_vpn(self,
                      user: User,
                      vpn_type: VpnType = VpnType.VLESS,
                      create_if_not_exists: bool = True
                      ) -> Optional[VpnConfig]: ...

    @abc.abstractmethod
    async def toggle_active(self,
                            user: User,
                            delete: bool = False
                            ) -> bool: ...

    @abc.abstractmethod
    async def get_inbounds(self,
                       user: User
                       ) -> list[AccessConfig]: ...
    
    @abc.abstractmethod
    async def get_traffic(self, user: User) -> int: ...

    @abc.abstractmethod
    async def reset_traffic(self, user: User) -> bool: ...
