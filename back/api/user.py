

from fastapi import Cookie, Depends, HTTPException
from fastapi_controllers import Controller, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from back.get_auth import get_user
from back.schemas.user_scheme import EditUserScheme, UserScheme
from database.database import get_db_session
from database.models.user import User
from database.repositories.user_repository import UserRepository


class UserController(Controller):
    prefix = '/user'
    tags = ['user']

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:    
        self.session = session

    @get("/get_all")
    async def get_all(self, user: User = Depends(get_user)) -> list[UserScheme]:
        if user.is_control_panel_user is False:
            raise HTTPException(status_code=403, detail="user is not control panel member")
        ur = UserRepository(self.session)
        users = await ur.get_all()
        users_to_send = []
        for user in users:
            user_to_send = UserScheme(id=user.id,
                                       telegram_id=user.telegram_id,
                                       telegram_username=user.telegram_username,
                                       balance=user.balance,
                                       created_date=user.created_date.isoformat(),
                                       is_server_editor=user.is_server_editor,
                                       is_transaction_editor=user.is_transaction_editor,
                                       is_active_period_editor=user.is_active_period_editor,
                                       is_tariff_editor=user.is_tariff_editor,
                                       is_member_rights_editor=user.is_member_rights_editor,
                                       is_admin_rights_editor=user.is_admin_rights_editor,
                                       is_control_panel_user=user.is_control_panel_user,
                                       is_active=user.is_active,
                                       verified=user.verified,
                                       auto_pay=user.auto_pay)
            users_to_send.append(user_to_send)
        return users_to_send
    
    @post("/edit")
    async def edit_user(self, user_to_edit: EditUserScheme, user: User = Depends(get_user)):
        if user.is_control_panel_user is False:
            raise HTTPException(status_code=403, detail="no rights")
        if user.is_user_editor is False:
            raise HTTPException(status_code=403, detail="no rights")
        if user_to_edit.is_admin_rights_editor is True and user.is_admin_rights_editor is False:
            raise HTTPException(status_code=403, detail="no rights")
        if user_to_edit.is_member_rights_editor is True and user.is_member_rights_editor is False:
            raise HTTPException(status_code=403, detail="no rights")
        

        
        