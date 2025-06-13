

from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import User, UserRepository, session_manager
from shared.infrastructure import RedisType, get_redis_client

from ..config import Config
from ..get_auth import get_user, get_user_db
from ..schemas import EditUserSchema, UserSchema

router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    path="/all",
    summary="Get all users"
)
async def get_all(user: UserSchema = Depends(get_user),
                  session: AsyncSession = Depends(session_manager.session)
                  ) -> list[UserSchema]:
    if user.rights.is_control_panel_user is False:
        raise HTTPException(
            status_code=403, detail="user is not control panel member")
    ur = UserRepository(session)
    users = await ur.get_all()
    users_to_send: list[UserSchema] = []
    for u in users:
        users_to_send.append(UserSchema.from_db(u))
    return users_to_send


@router.patch(
    path="/{user_id}",
    summary="Edit user")
async def edit_user(user_to_edit: EditUserSchema,
                    user: User = Depends(get_user_db),
                    redis: Redis = Depends(get_redis_client),
                    session: AsyncSession = Depends(session_manager.session)
                    ):  # TODO: fix method
    redis.set(f"{RedisType.invalidated_access_token}:{user.id}",
              1, ex=Config.access_token_lifetime)
    ur = UserRepository(session)
    if user_to_edit.rights is not None:
        if user.is_control_panel_user is False:
            raise HTTPException(status_code=403, detail="no rights")
        if user.is_user_editor is False:
            raise HTTPException(status_code=403, detail="no rights")
        if user_to_edit.rights.is_admin_rights_editor is not None or user.is_admin_rights_editor is False:
            raise HTTPException(status_code=403, detail="no rights")
        if user_to_edit.rights.is_member_rights_editor is True or user.is_member_rights_editor is False:
            raise HTTPException(status_code=403, detail="no rights")
        await ur.update_rights(user, user_to_edit.rights.model_dump())

    if user_to_edit.settings is not None:
        if len(user_to_edit.settings.model_dump()) > 0 and user.is_user_editor is False:
            raise HTTPException(status_code=403, detail="no rights")
        await ur.update_settings(user, user_to_edit.settings.model_dump())

    if user_to_edit.telegram_id is not None:
        if user.is_user_editor is False:
            raise HTTPException(status_code=403, detail="no rights")
        await ur.update_telegram_id(user, user_to_edit.telegram_id)

    if user_to_edit.created_date is not None:
        if user.is_user_editor is False:
            raise HTTPException(status_code=403, detail="no rights")

    return {'message': 'OK'}


@router.get(
    path="",
    summary="Get self info")
async def get_self_info(user: UserSchema = Depends(get_user)
                        ) -> UserSchema:
    return user
