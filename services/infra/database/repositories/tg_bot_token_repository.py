

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models import Server, TgBotToken

from .base_repository import BaseRepository


class TgBotTokenRepository(BaseRepository[TgBotToken]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TgBotToken)

    async def create(self,
                     token: str,
                     server: Server
                     ) -> TgBotToken:
        return await self.universal_create(
            token=token,
            server_id=server.id)

    async def get_by_server(self, 
                            server: Server
                            ) -> TgBotToken | None:
        stmt = select(TgBotToken).where(
            TgBotToken.server_id == server.id).limit(1)
        return await self.session.scalar(stmt)
