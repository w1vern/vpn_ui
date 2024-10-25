from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.database.models import *
from typing import Optional
from datetime import datetime, UTC


class ServerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, ip: str, panel_path: str, country_code: str, display_name: str, login: str, password:str, created_date: datetime = datetime.now(UTC).replace(tzinfo=None), is_available: bool = True) -> None:
        server = Server(ip=ip, panel_path=panel_path, country_code=country_code, is_available=is_available, display_name=display_name, created_date=created_date, login=login, password=password)
        self.session.add(server)
        await self.session.flush()

    async def get_by_id(self, id: UUID) -> Optional[Server]:
        stmt = select(Server).where(Server.id==id).limit(1)
        return await self.session.scalar(stmt)
    
    async def get_all(self) -> list[Server]:
        stmt = select(Server)
        return list((await self.session.scalars(stmt)).all())