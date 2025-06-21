

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from ..response import SuccessResponse
from ..schemas import (
    EditUserSchema,
    UserSchema,
)
from ..services import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    path="/all",
    summary="Get all users"
)
async def all(user_service: UserService = Depends(UserService.depends)
              ) -> list[UserSchema]:
    return await user_service.all()


@router.patch(
    path="/{user_id}",
    summary="Edit user")
async def edit_user(user_id: UUID,
                    edited_user: EditUserSchema,
                    user_service: UserService = Depends(UserService.depends)
                    ) -> SuccessResponse:
    await user_service.edit(user_id, edited_user)
    return SuccessResponse()


@router.get(
    path="",
    summary="Get self info")
async def get_self_info(user_service: UserService = Depends(UserService.depends)
                        ) -> UserSchema:
    return await user_service.get_self_info()
