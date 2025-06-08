
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import ServerUserInbound, Server, User
from services.infra.interfaces.proxy.models import AccessConfig, AccessType

from .base_repository import BaseRepository


class ServerUserInboundRepository(BaseRepository[ServerUserInbound]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self,
                     server: Server,
                     user: User,
                     config: AccessConfig,
                     ) -> ServerUserInbound:
        return await self.universal_create(
            server_id=server.id,
            user_id=user.id,
            config_str=config.to_string()
        )

    async def get_by_server_and_user(self,
                                     server: Server,
                                     user: User
                                     ) -> list[ServerUserInbound]:
        stmt = select(ServerUserInbound
                      ).where(ServerUserInbound.server_id == server.id,
                              ServerUserInbound.user_id == user.id)
        return list((await self.session.scalars(stmt)).all())

    async def get_by_server_user_access_type(self, 
                                             server: Server, 
                                             user: User, 
                                             access_type: AccessType
                                             ) -> ServerUserInbound | None:
        stmt = select(ServerUserInbound
                      ).where(ServerUserInbound.server_id == server.id,
                              ServerUserInbound.user_id == user.id)
        all = list((await self.session.scalars(stmt)).all())
        for inbound in all:
            if inbound.access_type == access_type:
                return inbound
        return None

    async def update_inbound(self,
                             id: uuid.UUID,
                             access_config: AccessConfig,
                             ) -> None:
        server_user_inbounds = await self.get_by_id(id)
        if server_user_inbounds is None:
            return
        server_user_inbounds.config_str = access_config.to_string()
        await self.session.flush()
