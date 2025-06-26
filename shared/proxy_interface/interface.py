

import abc

from shared.database.models.user import User

from .models import (
    AccessConfig,
    AccessType,
)


class ProxyInterface(abc.ABC):

    @abc.abstractmethod
    async def get_config(self,
                         user: User,
                         access_type: AccessType = AccessType.HTTP,
                         create_if_not_exists: bool = True,
                         login: str = "",
                         password: str = ""
                         ) -> AccessConfig | None: ...

    @abc.abstractmethod
    async def set_enable(self,
                         user: User,
                         enable: bool,
                         access_type: AccessType | None = None,
                         ) -> None: ...

    @abc.abstractmethod
    async def delete(self, user: User, access_type: AccessType) -> None: ...

    @abc.abstractmethod
    async def get_configs(self, user: User) -> list[AccessConfig]: ...

    @abc.abstractmethod
    async def get_traffic(self, user: User) -> int: ...

    @abc.abstractmethod
    async def reset_traffic(self, user: User) -> None: ...
