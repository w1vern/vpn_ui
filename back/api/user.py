

from datetime import datetime

from fastapi import Cookie, Depends, HTTPException
from fastapi_controllers import Controller, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from back.get_auth import get_user
from back.schemas.user import (EditUserScheme, UserRightsScheme, UserScheme,
                               UserSettingsScheme)
from database.database import get_db_session
from database.models.user import User
from database.repositories.user_repository import UserRepository


class UserController(Controller):
    prefix = '/user'
    tags = ['user']

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    @get("/get_all")
    async def get_all(self,
                      user: User = Depends(get_user)
                      ) -> list[UserScheme]:
        if user.is_control_panel_user is False:
            raise HTTPException(
                status_code=403, detail="user is not control panel member")
        ur = UserRepository(self.session)
        users = await ur.get_all()
        users_to_send = []
        for user in users:
            user_settings = UserSettingsScheme(
                auto_pay=user.auto_pay,
                is_active=user.is_active,
                get_traffic_notifications=user.get_traffic_notifications)
            user_rights = UserRightsScheme(
                is_server_editor=user.is_server_editor,
                is_transaction_editor=user.is_transaction_editor,
                is_active_period_editor=user.is_active_period_editor,
                is_tariff_editor=user.is_tariff_editor,
                is_member_rights_editor=user.is_member_rights_editor,
                is_admin_rights_editor=user.is_admin_rights_editor,
                is_control_panel_user=user.is_control_panel_user,
                is_verified=user.is_verified)
            user_to_send = UserScheme(
                id=user.id,
                telegram_id=user.telegram_id,
                telegram_username=user.telegram_username,
                balance=user.balance,
                created_date=user.created_date.isoformat(),
                rights=user_rights,
                settings=user_settings)
            users_to_send.append(user_to_send)
        return users_to_send

    @post("/edit")
    async def edit_user(self,
                        user_to_edit: EditUserScheme,
                        user: User = Depends(get_user)):
        ur = UserRepository(self.session)
        if user_to_edit.rights is not None:
            if user.is_control_panel_user is False:
                raise HTTPException(status_code=403, detail="no rights")
            if user.is_user_editor is False:
                raise HTTPException(status_code=403, detail="no rights")
            if user_to_edit.rights.is_admin_rights_editor is not None and user.is_admin_rights_editor is False:
                raise HTTPException(status_code=403, detail="no rights")
            if user_to_edit.rights.is_member_rights_editor is True and user.is_member_rights_editor is False:
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
