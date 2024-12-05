

import abc
from typing import Optional

from database.models.user import User
from .models import ProxyConfig, ProxyType, VpnConfig, VpnType, AccessConfig, AccessType


class ProxyInterface(abc.ABC):

    @abc.abstractmethod
    async def get_config(self,
                          user: User,
                          access_type: AccessType = AccessType.HTTP,
                          create_if_not_exists: bool = True,
                          login: str = "",
                          password: str = ""
                          ) -> Optional[AccessConfig]: ...

    @abc.abstractmethod
    async def toggle_active(self,
                            user: User,
                            access_type: Optional[AccessType] = None,
                            delete: bool = False
                            ) -> None: ...

    @abc.abstractmethod
    async def get_configs(self, user: User) -> list[AccessConfig]: ...

    @abc.abstractmethod
    async def get_traffic(self, user: User) -> int: ...

    @abc.abstractmethod
    async def reset_traffic(self, user: User) -> None: ...
