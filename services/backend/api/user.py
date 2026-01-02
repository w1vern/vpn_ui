
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from ..response import SuccessResponse
from ..schemas import EditUserSchema, UserSchema
from ..services import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    path="",
    summary="Get all users"
)
async def all(
    offset: int | None = Query(None,
                               ge=0,
                               description="From which index to start"),
    limit: int | None = Query(None,
                              ge=1,
                              description="Number of items to return"),
    user_service: UserService = Depends(UserService.depends)
) -> list[UserSchema]:
    return await user_service.all(limit, offset)


@router.get(
    path="/count",
    summary="Get users count"
)
async def count(
    user_service: UserService = Depends(UserService.depends)
) -> int:
    return await user_service.count()


@router.patch(
    path="/{user_id}",
    summary="Edit user")
async def edit_user(
    user_id: UUID,
    edited_user: EditUserSchema,
    user_service: UserService = Depends(UserService.depends)
) -> SuccessResponse:
    await user_service.edit(user_id, edited_user)
    return SuccessResponse()


@router.get(
    path="/me",
    summary="Get self info")
async def get_self_info(
    user_service: UserService = Depends(UserService.depends)
) -> UserSchema:
    return await user_service.get_self_info()


@router.get(
    path="/{user_id}",
    summary=""
)
async def get_user(
    user_id: UUID,
    user_service: UserService = Depends(UserService.depends)
) -> UserSchema:
    return await user_service.get(user_id)
