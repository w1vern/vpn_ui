

from fastapi import Depends, HTTPException
from fastapi_controllers import Controller, get, post
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db_session
from app.database.repositories.server_repository import ServerRepository
from app.site.schemes.server_scheme import ServerToCreate


class ServerController(Controller):
    prefix='server'
    tags=['server']

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    @post('')
    async def create_server(self, server: ServerToCreate):
        sr = ServerRepository(self.session)
        duplicate = await sr.get_by_id(server.id)
        if not duplicate is None:
            raise HTTPException(status_code=400, detail='server already exists')
        sr.create()


        