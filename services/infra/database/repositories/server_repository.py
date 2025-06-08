
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models import *

from .base_repository import BaseRepository


class ServerRepository(BaseRepository[Server]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Server)

    async def create(self,
                     ip: str,
                     country_code: str,
                     display_name: str,
                     starting_date: datetime | None = None,
                     closing_date: datetime | None = None,
                     is_available: bool = True
                     ) -> Server:
        if starting_date is None:
            starting_date = datetime.now(UTC).replace(tzinfo=None)
        if closing_date is None:
            closing_date = datetime.min
        return await self.universal_create(
            ip=ip,
            country_code=country_code,
            is_available=is_available,
            display_name=display_name,
            starting_date=starting_date,
            closing_date=closing_date)

    async def set_is_available(self,
                               server: Server,
                               is_available: bool
                               ) -> None:
        server.is_available = is_available
        await self.session.flush()

    async def set_created_date(self,
                               server: Server,
                               created_date: datetime
                               ) -> None:
        server.created_date = created_date
        await self.session.flush()

    async def set_closing_date(self,
                               server: Server,
                               closing_date: datetime
                               ) -> None:
        server.closing_date = closing_date
        await self.session.flush()

    async def set_display_name(self,
                               server: Server,
                               display_name: str
                               ) -> None:
        server.display_name = display_name
        await self.session.flush()

    async def set_ip(self,
                     server: Server,
                     ip: str
                     ) -> None:
        server.ip = ip
        await self.session.flush()

    async def set_country_code(self,
                               server: Server,
                               country_code: str
                               ) -> None:
        server.country_code = country_code
        await self.session.flush()
