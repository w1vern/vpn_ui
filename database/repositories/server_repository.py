from datetime import UTC, datetime, timedelta
import json
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import *


class ServerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self,
                     ip: str,
                     country_code: str,
                     display_name: str,
                     created_date: Optional[datetime] = None,
                     closing_date: Optional[datetime] = None,
                     is_available: bool = True
                     ) -> Optional[Server]:
        if created_date is None:
            created_date = datetime.now(UTC).replace(tzinfo=None)
        if closing_date is None:
            closing_date = (datetime.now(UTC) +
                            timedelta(days=30)).replace(tzinfo=None)
        server = Server(ip=ip,
                        country_code=country_code,
                        is_available=is_available,
                        display_name=display_name,
                        created_date=created_date,
                        closing_date=closing_date)
        self.session.add(server)
        await self.session.flush()
        return await self.get_by_id(server.id)

    async def get_by_id(self, id: UUID) -> Optional[Server]:
        stmt = select(Server).where(Server.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_all(self) -> Sequence[Server]:
        stmt = select(Server)
        return list((await self.session.scalars(stmt)).all())
