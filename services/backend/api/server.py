
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from ..response import SuccessResponse
from ..schemas import (
    CreateServerSchema,
    ServerSchema,
    ServerToEditSchema,
)
from ..services import ServerService

router = APIRouter(prefix="/servers", tags=["servers"])


@router.get(
    path="",
    summary="Get all servers"
)
async def get_all(
    offset: int | None = Query(None,
                               ge=0,
                               description="From which index to start"),
    limit: int | None = Query(None,
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
    summary="Create a new server",
)
async def create_server(
    server_to_create: CreateServerSchema,
    server_service: ServerService = Depends(
        ServerService.depends)
) -> SuccessResponse:
    await server_service.create(server_to_create)
    return SuccessResponse()


@router.patch(
    path="/{server_id}",
    summary="Update an existing server",
)
async def edit_server(
    server_id: UUID,
    server_to_edit: ServerToEditSchema,
    server_service: ServerService = Depends(
        ServerService.depends)
) -> SuccessResponse:
    await server_service.edit(server_id, server_to_edit)
    return SuccessResponse()
