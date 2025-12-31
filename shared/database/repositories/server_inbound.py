
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UNSET, Server, ServerInbound, Unset
from .base import BaseRepository


class ServerInboundRepository(BaseRepository[ServerInbound]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ServerInbound)

    async def create(
        self,
        server: Server,
        inbound_id: int,
        template: str,
        protocol: str,
        name: str,
        description: str,
        is_available: bool
    ) -> ServerInbound:
        return await self._create(
            server_id=server.id,
            inbound_id=inbound_id,
            template=template,
            protocol=protocol,
            name=name,
            description=description,
            is_available=is_available
        )
        
    async def edit(
        self,
        server_inbound: ServerInbound,
        *,
        template: str | Unset = UNSET,
        protocol: str | Unset = UNSET,
        name: str | Unset = UNSET,
        description: str | Unset = UNSET,
        is_available: bool | Unset = UNSET
    ) -> None:
        await self._edit(
            server_inbound,
            template=template,
            protocol=protocol,
            name=name,
            description=description,
            is_available=is_available
        )