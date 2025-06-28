

from uuid import UUID

from fastapi import APIRouter, Depends

from ..response import SuccessResponse
from ..schemas import (
    CreateServerSchema,
    ServerSchema,
    ServerToEditSchema,
)
from ..services import ServerService

router = APIRouter(prefix="/server", tags=["server"])


@router.get(
    path="/all",
    summary="Get all servers"
)
async def get_all(server_service: ServerService = Depends(ServerService.depends)
                  ) -> list[ServerSchema]:
    return await server_service.all()


@router.post(
    path="",
    summary="Create a new server",
)
async def create_server(server_to_create: CreateServerSchema,
                        server_service: ServerService = Depends(
                            ServerService.depends)
                        ) -> SuccessResponse:
    await server_service.create(server_to_create)
    return SuccessResponse()


@router.patch(
    path="/{server_id}",
    summary="Update an existing server",
)
async def edit_server(server_id: UUID,
                      server_to_edit: ServerToEditSchema,
                      server_service: ServerService = Depends(
                          ServerService.depends)
                      ) -> SuccessResponse:
    await server_service.edit(server_id, server_to_edit)
    return SuccessResponse()
