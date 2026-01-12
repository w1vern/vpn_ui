
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import ServerRepository, Unset, UserRepository

from ..depends import (
    get_server_repo,
    get_session,
    get_user,
    get_user_repo
)
from ..exceptions import (
    NotServerEditorException,
    ServerNotFoundException
)
from ..schemas import (
    CreateServerSchema,
    EditServerSchema,
    ServerSchema,
    UserSchema
)


class ServerService:
    def __init__(
        self,
        session: AsyncSession,
        ur: UserRepository,
        sr: ServerRepository,
        user_schema: UserSchema
    ) -> None:
        self.session = session
        self.ur = ur
        self.sr = sr
        self.user_schema = user_schema

    @classmethod
    def depends(
        cls,
        session: AsyncSession = Depends(get_session),
        ur: UserRepository = Depends(get_user_repo),
        sr: ServerRepository = Depends(get_server_repo),
        user_schema: UserSchema = Depends(get_user)
    ) -> 'ServerService':
        return cls(session, ur, sr, user_schema)

    async def all(
        self,
        limit: int | None,
        offset: int | None
    ) -> list[ServerSchema]:
        return [ServerSchema.from_db(s)
                for s in await self.sr.get_all(limit, offset)]

    async def count(self) -> int:
        return await self.sr.count()

    async def get(
        self,
        server_id: UUID
    ) -> ServerSchema:
        server = await self.sr.get_by_id(server_id)
        if server is None:
            raise ServerNotFoundException()
        return ServerSchema.from_db(server)

    async def create(
        self,
        server_to_create: CreateServerSchema
    ) -> ServerSchema:
        if self.user_schema.rights.is_servers_editor is False:
            raise NotServerEditorException()
        server = await self.sr.create(
            ip=server_to_create.ip,
            secured=server_to_create.secured,
            description=server_to_create.description,
            country_code=server_to_create.country_code,
            display_name=server_to_create.display_name,
            panel_port=server_to_create.panel_port,
            panel_web_path=server_to_create.panel_web_path,
            panel_login=server_to_create.panel_login,
            panel_password=server_to_create.panel_password,
            starting_date=server_to_create.starting_date.replace(
                tzinfo=None),
            closing_date=server_to_create.closing_date.replace(tzinfo=None))
        return ServerSchema.from_db(server)

    async def edit(
        self,
        server_id: UUID,
        server_to_edit: EditServerSchema
    ) -> ServerSchema:
        if self.user_schema.rights.is_servers_editor is False:
            raise NotServerEditorException()
        server = await self.sr.get_by_id(server_id)
        if server is None:
            raise ServerNotFoundException()
        if not isinstance(server_to_edit.starting_date, Unset):
            server_to_edit.starting_date = server_to_edit.starting_date.replace(
                tzinfo=None)
        if not isinstance(server_to_edit.closing_date, Unset):
            server_to_edit.closing_date = server_to_edit.closing_date.replace(
                tzinfo=None)
        await self.sr.edit(
            server,
            ip=server_to_edit.ip,
            secured=server_to_edit.secured,
            description=server_to_edit.description,
            country_code=server_to_edit.country_code,
            display_name=server_to_edit.display_name,
            panel_port=server_to_edit.panel_port,
            panel_web_path=server_to_edit.panel_web_path,
            panel_login=server_to_edit.panel_login,
            panel_password=server_to_edit.panel_password,
            starting_date=server_to_edit.starting_date,
            closing_date=server_to_edit.closing_date
        )
        return ServerSchema.from_db(server)
