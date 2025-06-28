
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from ..response import SuccessResponse
from ..schemas import (
    CreateTariffSchema,
    EditTariffSchema,
    TariffSchema
)
from ..services import TariffService

router = APIRouter(prefix="/tariff", tags=["tariff"])


@router.get(
    path="/all",
    summary="Get all tariffs"
)
async def all(tariff_service: TariffService = Depends(TariffService.depends)
              ) -> list[TariffSchema]:
    return await tariff_service.all()


@router.get(
    path="/{tariff_id}",
    summary="Get tariff by id"
)
async def get(tariff_id: UUID, tariff_service: TariffService = Depends(TariffService.depends)
              ) -> TariffSchema:
    return await tariff_service.get(tariff_id)


@router.post(
    path="",
    summary="Create a new tariff"
)
async def create(create_tariff_schema: CreateTariffSchema,
                 tariff_service: TariffService = Depends(TariffService.depends)
                 ) -> SuccessResponse:
    await tariff_service.create(create_tariff_schema)
    return SuccessResponse()


@router.delete(
    path="/{tariff_id}",
    summary="Delete an existing tariff"
)
async def delete(tariff_id: UUID,
                 tariff_service: TariffService = Depends(TariffService.depends)
                 ) -> SuccessResponse:
    await tariff_service.delete(tariff_id)
    return SuccessResponse()


@router.patch(
    path="/{tariff_id}",
    summary="Edit an existing tariff"
)
async def edit(tariff_id: UUID, edited_tariff: EditTariffSchema,
               tariff_service: TariffService = Depends(TariffService.depends)
               ) -> SuccessResponse:
    await tariff_service.edit(tariff_id, edited_tariff)
    return SuccessResponse()
