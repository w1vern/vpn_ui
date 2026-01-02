
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from ..response import SuccessResponse
from ..schemas import (
    CreateServerInboundSchema,
    CreateServerSchema,
    EditServerInboundSchema,
    EditServerSchema,
    ServerInboundSchema,
    ServerSchema
)
from ..services import ServerInboundService, ServerService

router = APIRouter(prefix="/servers", tags=["servers"])


@router.get(
    path="/inbounds",
    summary="Get all server inbounds"
)
async def get_all_inbounds(
    server_id: UUID | None = Query(None, description="Server ID"),
    offset: int | None = Query(
        None,
        ge=0,
        description="From which index to start"),
    limit: int | None = Query(
        None,
        ge=1,
        description="Number of items to return"),
    server_ibound_service: ServerInboundService = Depends(
        ServerInboundService.depends)
) -> list[ServerInboundSchema]:
    return await server_ibound_service.all(server_id, limit, offset)


@router.get(
    path="/inbounds/count",
    summary="Get server inbounds count"
)
async def count_inbounds(
    server_id: UUID | None = Query(None, description="Server ID"),
    server_ibound_service: ServerInboundService = Depends(
        ServerInboundService.depends)
) -> int:
    return await server_ibound_service.count(server_id)


@router.post(
    path="/inbounds/{server_id}",
    summary="Create a new server inbound"
)
async def create_server_inbound(
    server_id: UUID,
    server_inbound_to_create: CreateServerInboundSchema,
    server_ibound_service: ServerInboundService = Depends(
        ServerInboundService.depends)
) -> ServerInboundSchema:
    return await server_ibound_service.create(server_id, server_inbound_to_create)


@router.get(
    path="/inbounds/{server_inbound_id}",
    summary="Get server inbound by id"
)
async def get_server_inbound(
    server_inbound_id: UUID,
    server_ibound_service: ServerInboundService = Depends(
        ServerInboundService.depends)
) -> ServerInboundSchema:
    return await server_ibound_service.get(server_inbound_id)


@router.patch(
    path="/inbounds/{server_inbound_id}",
    summary="Update an existing server inbound"
)
async def edit_server_inbound(
    server_inbound_id: UUID,
    server_inbound_to_edit: EditServerInboundSchema,
    server_ibound_service: ServerInboundService = Depends(
        ServerInboundService.depends)
) -> SuccessResponse:
    await server_ibound_service.edit(server_inbound_id, server_inbound_to_edit)
    return SuccessResponse()


@router.get(
    path="",
    summary="Get all servers"
)
async def get_all(
    offset: int | None = Query(
        None,
        ge=0,
        description="From which index to start"),
    limit: int | None = Query(
        None,
        ge=1,
        description="Number of items to return"),
    server_service: ServerService = Depends(ServerService.depends)
) -> list[ServerSchema]:
    return await server_service.all(limit, offset)


@router.get(
    path="/count",
    summary="Get servers count"
)
async def count(
    server_service: ServerService = Depends(ServerService.depends)
) -> int:
    return await server_service.count()


@router.get(
    path="/{server_id}",
    summary="Get server by id"
)
async def get_server(
    server_id: UUID,
    server_service: ServerService = Depends(ServerService.depends)
) -> ServerSchema:
    return await server_service.get(server_id)


@router.post(
    path="",
    summary="Create a new server"
)
async def create_server(
    server_to_create: CreateServerSchema,
    server_service: ServerService = Depends(
        ServerService.depends)
) -> ServerSchema:
    return await server_service.create(server_to_create)


@router.patch(
    path="/{server_id}",
    summary="Update an existing server"
)
async def edit_server(
    server_id: UUID,
    server_to_edit: EditServerSchema,
    server_service: ServerService = Depends(
        ServerService.depends)
) -> SuccessResponse:
    await server_service.edit(server_id, server_to_edit)
    return SuccessResponse()
