

from datetime import datetime

from back.config import Config
from back.get_auth import get_user, get_user_db
from back.schemas.user import (EditUserSchema, UserRightsSchema, UserSchema,
                               UserSettingsSchema)
from fastapi import Cookie, Depends, HTTPException
from fastapi_controllers import Controller, get, post
from infra.database.main import get_db_session
from infra.database.models.user import User
from infra.database.redis import RedisType, get_redis_client
from infra.database.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserController(Controller):
    prefix = '/user'
    tags = ['user']

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    @get("/get_all")
    async def get_all(self,
                      user: UserSchema = Depends(get_user)
                      ) -> list[UserSchema]:
        if user.rights.is_control_panel_user is False:
            raise HTTPException(
                status_code=403, detail="user is not control panel member")
        ur = UserRepository(self.session)
        users = await ur.get_all()
        users_to_send = []
        for u in users:
            users_to_send.append(UserSchema.from_db(u))
        return users_to_send

    @post("/edit")
    async def edit_user(self,
                        user_to_edit: EditUserSchema,
                        user: User = Depends(get_user_db),
                        redis=Depends(get_redis_client)): #TODO: fix method
        redis.set(f"{RedisType.invalidated_access_token}:{user.id}", 1, ex=Config.access_token_lifetime)
        ur = UserRepository(self.session)
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
            await ur.update_created_date(user, datetime.fromisoformat(user_to_edit.created_date))

        return {'message': 'OK'}
