
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    Protocols,
    ServerInboundRepository,
    ServerRepository
)

from ..depends import (
    get_server_inbound_repo,
    get_server_repo,
    get_session,
    get_user
)
from ..exceptions import (
    NotServerEditorException,
    ServerInboundNotFoundException,
    ServerNotFoundException
)
from ..schemas import (
    CreateServerInboundSchema,
    EditServerInboundSchema,
    ProtocolsSchema,
    ServerInboundSchema,
    UserSchema
)


class ServerInboundService:
    def __init__(
        self,
        session: AsyncSession,
        sr: ServerRepository,
        sir: ServerInboundRepository,
        user_schema: UserSchema
    ) -> None:
        self.session = session
        self.sr = sr
        self.sir = sir
        self.user_schema = user_schema

    @classmethod
    def depends(
        cls,
        session: AsyncSession = Depends(get_session),
        sr: ServerRepository = Depends(get_server_repo),
        sir: ServerInboundRepository = Depends(get_server_inbound_repo),
        user_schema: UserSchema = Depends(get_user)
    ) -> 'ServerInboundService':
        return cls(session, sr, sir, user_schema)

    async def get(
        self,
        inbound_id: UUID
    ) -> ServerInboundSchema:
        inbound = await self.sir.get_by_id(inbound_id)
        if inbound is None:
            raise ServerInboundNotFoundException
        return ServerInboundSchema.from_db(inbound)

    async def all(
        self,
        server_id: UUID | None,
        limit: int | None,
        offset: int | None
    ) -> list[ServerInboundSchema]:
        return [ServerInboundSchema.from_db(inbound)
                for inbound in
                await self.sir.get_all(
                    limit=limit,
                    offset=offset,
                    server_id=server_id)]

    async def count(
        self,
        server_id: UUID | None
    ) -> int:
        return await self.sir.count(server_id=server_id)

    async def create(
        self,
        server_id: UUID,
        inbound_to_create: CreateServerInboundSchema
    ) -> ServerInboundSchema:
        if self.user_schema.rights.is_server_editor is False:
            raise NotServerEditorException()
        server = await self.sr.get_by_id(server_id)
        if server is None:
            raise ServerNotFoundException()
        inbound = await self.sir.create(
            server=server,
            inbound_id=inbound_to_create.inbound_id,
            template=inbound_to_create.template,
            protocol=inbound_to_create.protocol,
            name=inbound_to_create.name,
            description=inbound_to_create.description,
            is_available=inbound_to_create.is_available
        )
        return ServerInboundSchema.from_db(inbound)

    async def edit(
        self,
        server_inbound_id: UUID,
        server_inbound_to_edit: EditServerInboundSchema
    ) -> ServerInboundSchema:
        if self.user_schema.rights.is_server_editor is False:
            raise NotServerEditorException()
        server_inbound = await self.sir.get_by_id(server_inbound_id)
        if server_inbound is None:
            raise ServerInboundNotFoundException()
        await self.sir.edit(
            server_inbound,
            template=server_inbound_to_edit.template,
            protocol=server_inbound_to_edit.protocol,
            name=server_inbound_to_edit.name,
            description=server_inbound_to_edit.description,
            is_available=server_inbound_to_edit.is_available
        )
        return ServerInboundSchema.from_db(server_inbound)

    async def delete(
        self,
        server_inbound_id: UUID
    ) -> None:
        if self.user_schema.rights.is_server_editor is False:
            raise NotServerEditorException()
        server_inbound = await self.sir.get_by_id(server_inbound_id)
        if server_inbound is None:
            raise ServerInboundNotFoundException()
        await self.sir.delete(server_inbound)

    async def protocols(
        self
    ) -> ProtocolsSchema:
        return ProtocolsSchema(data={
            Protocols.vless: "vless://{user_id}@...#{comment}",
        })
