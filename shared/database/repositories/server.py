
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UNSET, Server, Unset
from .base import BaseRepository


class ServerRepository(BaseRepository[Server]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Server)

    async def create(
        self,
        ip: str,
        secured: bool,
        description: str,
        country_code: str,
        display_name: str,
        panel_port: int,
        panel_web_path: str,
        panel_login: str,
        panel_password: str,
        starting_date: datetime | None = None,
        closing_date: datetime | None = None
    ) -> Server:
        if starting_date is None:
            starting_date = datetime.now(UTC).replace(tzinfo=None)
        if closing_date is None:
            closing_date = datetime.min
        return await self._create(
            ip=ip,
            secured=secured,
            description=description,
            country_code=country_code,
            display_name=display_name,
            panel_port=panel_port,
            panel_web_path=panel_web_path,
            panel_login=panel_login,
            panel_password=panel_password,
            starting_date=starting_date,
            closing_date=closing_date
        )
        
    async def edit(
        self,
        server: Server,
        *,
        ip: str | Unset = UNSET,
        secured: bool | Unset = UNSET,
        description: str | Unset = UNSET,
        country_code: str | Unset = UNSET,
        display_name: str | Unset = UNSET,
        panel_port: int | Unset = UNSET,
        panel_web_path: str | Unset = UNSET,
        panel_login: str | Unset = UNSET,
        panel_password: str | Unset = UNSET,
        starting_date: datetime | Unset = UNSET,
        closing_date: datetime | Unset = UNSET
    ) -> None:
        await self._edit(
            server,
            ip=ip,
            secured=secured,
            description=description,
            country_code=country_code,
            display_name=display_name,
            panel_port=panel_port,
            panel_web_path=panel_web_path,
            panel_login=panel_login,
            panel_password=panel_password,
            starting_date=starting_date,
            closing_date=closing_date
        )
