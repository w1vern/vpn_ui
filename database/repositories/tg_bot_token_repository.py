

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.server import Server
from database.models.tg_bot_token import TgBotToken


class TgBotTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, token: str, server: Server) -> TgBotToken | None:
        tg_bot_token = TgBotToken(token=token, server_id=server.id)
        self.session.add(tg_bot_token)
        await self.session.flush()
        return await self.get_by_id(tg_bot_token.id)
    
    async def get_by_id(self, id: uuid.UUID) -> TgBotToken | None:
        stmt = select(TgBotToken).where(TgBotToken.id == id).limit(1)
        return await self.session.scalar(stmt)
    
    async def get_by_server(self, server: Server) -> TgBotToken | None:
        stmt = select(TgBotToken).where(TgBotToken.server_id == server.id).limit(1)
        return await self.session.scalar(stmt)