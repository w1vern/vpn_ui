



from fastapi import Depends
from fastapi_controllers import Controller, get
from sqlalchemy.ext.asyncio import AsyncSession

from back.get_auth import get_user
from database.database import get_db_session
from database.models.user import User
from database.repositories.user_repository import UserRepository


class UserController(Controller):
    prefix = "/user"
    tags = ["user"]

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    @get("/all")
    async def get_all_users(self, user: User = Depends(get_user)):
        ur = UserRepository(self.session)
        