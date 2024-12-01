import secrets
from datetime import UTC, datetime
from secrets import token_urlsafe
from typing import Optional
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.enums.role import Role
from database.models import *


class ServerUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, server: Server, user: User, vless_id: uuid.UUID = uuid.UUID(int=0), 
                     vless_reality_id: uuid.UUID = uuid.UUID(int=0), vmess_id: uuid.UUID = uuid.UUID(int=0), 
                     http_id: int = 0, socks_id: int = 0
                     ) -> Optional[ServerUserInbound]:
        server_user = ServerUserInbound(
            server=server,
            user=user,
            vless_id=vless_id,
            vless_reality_id=vless_reality_id,
            vmess_id=vmess_id,
            http_id=http_id,
            socks_id=socks_id
        )
        self.session.add(server_user)
        await self.session.flush()
        return await self.get_by_id(server_user.server_id, server_user.user_id)

    async def get_by_id(self, server_id: uuid.UUID, user_id: uuid.UUID) -> Optional[ServerUserInbound]:
        stmt = select(ServerUserInbound).where(ServerUserInbound.server_id == server_id, ServerUserInbound.user_id == user_id).limit(1)
        return await self.session.scalar(stmt)
    
    async def update_ids(self, server: Server, user: User, vless_id: uuid.UUID = uuid.UUID(int=0), 
                         vless_reality_id: uuid.UUID = uuid.UUID(int=0), vmess_id: uuid.UUID = uuid.UUID(int=0), 
                         http_id: int = 0, socks_id: int = 0
                         ) -> None:
        server_user = await self.get_by_id(server.id, user.id)
        if server_user is None:
            return
        server_user.vless_id = vless_id
        server_user.vless_reality_id = vless_reality_id
        server_user.vmess_id = vmess_id
        server_user.http_id = http_id
        server_user.socks_id = socks_id
        await self.session.flush()
    
    

