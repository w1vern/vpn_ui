
from typing import Optional
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.enums.role import Role
from database.models import *
from interface.proxy.models import AccessConfig, AccessType


class ServerUserInboundRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self,
                     server: Server,
                     user: User,
                     config: AccessConfig,
                     ) -> Optional[ServerUserInbound]:
        server_user_inbound = ServerUserInbound(
            server_id=server.id,
            user_id=user.id,
            config_str=config.to_string()
        )
        self.session.add(server_user_inbound)
        await self.session.flush()
        return await self.get_by_id(server_user_inbound.id)
    
    async def get_by_id(self, id:uuid.UUID) -> Optional[ServerUserInbound]:
        stmt = select(ServerUserInbound).where(ServerUserInbound.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_server_and_user(self, server: Server, user: User) -> list[ServerUserInbound]:
        stmt = select(ServerUserInbound
                      ).where(ServerUserInbound.server_id == server.id,
                              ServerUserInbound.user_id == user.id)
        return list((await self.session.scalars(stmt)).all())

    async def update_inbound(self,
                             id: uuid.UUID,
                             access_config: AccessConfig,
                             ) -> None:
        server_user_inbounds = await self.get_by_id(id)
        if server_user_inbounds is None:
            return
        server_user_inbounds.config_str = access_config.to_string()
        await self.session.flush()
