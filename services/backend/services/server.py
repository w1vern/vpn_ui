
from datetime import datetime
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    PanelServerRepository,
    ServerRepository,
    UserRepository
)

from ..exceptions import (
    NotControlPanelUserException,
    NotServerEditorException,
    ServerNotFoundException
)
from ..schemas import (
    ServerSchema,
    ServerToCreateSchema,
    ServerToEditSchema,
    UserSchema
)
from .depends import (
    get_panel_server_repo,
    get_server_repo,
    get_session,
    get_user,
    get_user_repo,
)


class ServerService:
    def __init__(self,
                 session: AsyncSession,
                 ur: UserRepository,
                 sr: ServerRepository,
                 psr: PanelServerRepository,
                 user_schema: UserSchema
                 ) -> None:
        self.session = session
        self.ur = ur
        self.sr = sr
        self.psr = psr
        self.user_schema = user_schema

    @classmethod
    def depends(cls,
                session: AsyncSession = Depends(get_session),
                ur: UserRepository = Depends(get_user_repo),
                sr: ServerRepository = Depends(get_server_repo),
                psr: PanelServerRepository = Depends(get_panel_server_repo),
                user_schema: UserSchema = Depends(get_user)
                ) -> 'ServerService':
        return cls(session, ur, sr, psr, user_schema)

    async def all(self) -> list[ServerSchema]:
        return [ServerSchema.from_db(s) for s in await self.psr.get_all()]

    async def create(self,
                     server_to_create: ServerToCreateSchema
                     ) -> None:
        if self.user_schema.rights.is_server_editor is False:
            raise NotServerEditorException()
        server = await self.sr.create(ip=server_to_create.ip,
                                      country_code=server_to_create.country_code,
                                      is_available=server_to_create.is_available,
                                      display_name=server_to_create.display_name,
                                      starting_date=datetime.fromisoformat(
                                          server_to_create.starting_date),
                                      closing_date=datetime.fromisoformat(
                                          server_to_create.closing_date))
        pserver = await self.psr.create(server=server,
                                        login=server_to_create.login,
                                        password=server_to_create.password,
                                        panel_path=server_to_create.panel_path)

    async def edit(self,
                   server_id: UUID,
                   server_to_edit: ServerToEditSchema
                   ) -> None:
        if self.user_schema.rights.is_server_editor is False:
            raise NotServerEditorException()
        server = await self.sr.get_by_id(server_id)
        pserver = await self.psr.get_by_id(server_id)
        if not (server and pserver):
            raise ServerNotFoundException()
        if server_to_edit.ip is not None:
            await self.sr.set_ip(server, server_to_edit.ip)
        if server_to_edit.country_code is not None:
            await self.sr.set_country_code(server, server_to_edit.country_code)
        if server_to_edit.display_name is not None:
            await self.sr.set_display_name(server, server_to_edit.display_name)
        if server_to_edit.created_date is not None:
            await self.sr.set_created_date(server, datetime.fromisoformat(server_to_edit.created_date))
        if server_to_edit.closing_date is not None:
            await self.sr.set_closing_date(server, datetime.fromisoformat(server_to_edit.closing_date))
        if server_to_edit.is_available is not None:
            await self.sr.set_is_available(server, server_to_edit.is_available)
        if server_to_edit.login is not None:
            await self.psr.set_login(pserver, server_to_edit.login)
        if server_to_edit.password is not None:
            await self.psr.set_password(pserver, server_to_edit.password)
        if server_to_edit.panel_path is not None:
            await self.psr.set_panel_path(pserver, server_to_edit.panel_path)
