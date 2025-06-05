
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import *
from interfaces.proxy.models import AccessConfig, AccessType


class ServerUserInboundRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self,
                     server: Server,
                     user: User,
                     config: AccessConfig,
                     ) -> ServerUserInbound | None:
        server_user_inbound = ServerUserInbound(
            server_id=server.id,
            user_id=user.id,
            config_str=config.to_string()
        )
        self.session.add(server_user_inbound)
        await self.session.flush()
        return await self.get_by_id(server_user_inbound.id)

    async def delete(self, id: uuid.UUID) -> None:
        stmt = select(ServerUserInbound).where(
            ServerUserInbound.id == id).limit(1)
        server_user_inbound = await self.session.scalar(stmt)
        if server_user_inbound is None:
            raise Exception()
        await self.session.delete(server_user_inbound)
        await self.session.flush()

    async def get_by_id(self, id: uuid.UUID) -> ServerUserInbound | None:
        stmt = select(ServerUserInbound).where(
            ServerUserInbound.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_server_and_user(self, server: Server, user: User) -> list[ServerUserInbound]:
        stmt = select(ServerUserInbound
                      ).where(ServerUserInbound.server_id == server.id,
                              ServerUserInbound.user_id == user.id)
        return list((await self.session.scalars(stmt)).all())
    
    async def get_by_server_user_access_type(self, server: Server, user: User, access_type: AccessType) -> ServerUserInbound | None:
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

    
