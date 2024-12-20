

import uuid
from datetime import datetime
from operator import is_
from typing import Sequence

from fastapi import Depends, HTTPException
from fastapi_controllers import Controller, delete, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from back.get_auth import get_user
from back.schemas.server import (EditServerScheme, ServerScheme,
                                 ServerToCreateScheme)
from database.database import get_db_session
from database.models.server import Server
from database.models.user import User
from database.repositories.panel_server_repository import PanelServerRepository
from database.repositories.server_repository import ServerRepository


class ServerController(Controller):
    prefix = "/server"
    tags = ["server"]

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    @get("/get_all")
    async def get_all(self, user: User = Depends(get_user)) -> list[ServerScheme]:
        if user.is_control_panel_user is False:
            raise HTTPException(
                status_code=403, detail="user is not control panel member")
        psr = PanelServerRepository(self.session)
        servers = await psr.get_all()
        result = []
        for server in servers:
            server_to_send = ServerScheme(
                id=server.id,
                display_name=server.display_name,
                ip=server.ip,
                country_code=server.country_code,
                is_available=server.is_available,
                created_date=server.created_date.isoformat(),
                closing_date=server.closing_date.isoformat(),
                panel_path=server.panel_path,
                login=server.login,
                password=server.password
            )
            result.append(server_to_send)
        return result

    @post("/create",
          summary="Create a new server",
          description=(
              "This endpoint allows the user to create a new server. "
              "If a server with the provided ID already exists, a 400 error is returned."
          ),
          responses={
              200: {"description": "Server successfully created"},
              400: {"description": "Server already exists"},
              401: {"description": "Unauthorized user"},
          },
          )
    async def create_server(self, server_to_create: ServerToCreateScheme, user: User = Depends(get_user)):
        if user.is_control_panel_user is False:
            raise HTTPException(
                status_code=403, detail="user is not control panel member")
        if user.is_server_editor is False:
            raise HTTPException(
                status_code=403, detail="user is not server editor")
        psr = PanelServerRepository(self.session)
        server = await psr.create(ip=server_to_create.ip,
                                  country_code=server_to_create.country_code,
                                  display_name=server_to_create.display_name,
                                  is_available=server_to_create.is_available,
                                  created_date=datetime.fromisoformat(
                                      server_to_create.created_date),
                                  closing_date=datetime.fromisoformat(
                                      server_to_create.closing_date),
                                  login=server_to_create.login,
                                  password=server_to_create.password,
                                  panel_path=server_to_create.panel_path)
        if server is None:
            raise HTTPException(status_code=400, detail="Server create error")
        return {"message": "OK"}

    @post("/edit",
          summary="Update an existing server",
          description=(
              "This endpoint allows the user to update an existing server's details. "
              "The new server data must be provided in the request body."
          ),
          responses={
              200: {"description": "Server successfully updated"},
              401: {"description": "Unauthorized user"},
              404: {"description": "Server not found"},
          },
          )
    async def edit_server(self, server_to_edit: EditServerScheme, user: User = Depends(get_user)):
        if user.is_control_panel_user is False:
            raise HTTPException(
                status_code=403, detail="user is not control panel member")
        if user.is_server_editor is False:
            raise HTTPException(
                status_code=403, detail="user is not server editor")
        psr = PanelServerRepository(self.session)
        server = await psr.get_by_id(server_to_edit.id)
        if server is None:
            raise HTTPException(status_code=404, detail="Server not found")
        if server_to_edit.ip is not None:
            await psr.set_ip(server, server_to_edit.ip)
        if server_to_edit.country_code is not None:
            await psr.set_country_code(server, server_to_edit.country_code)
        if server_to_edit.display_name is not None:
            await psr.set_display_name(server, server_to_edit.display_name)
        if server_to_edit.created_date is not None:
            await psr.set_created_date(server, datetime.fromisoformat(server_to_edit.created_date))
        if server_to_edit.closing_date is not None:
            await psr.set_closing_date(server, datetime.fromisoformat(server_to_edit.closing_date))
        if server_to_edit.is_available is not None:
            await psr.set_is_available(server, server_to_edit.is_available)
        if server_to_edit.login is not None:
            await psr.set_login(server, server_to_edit.login)
        if server_to_edit.password is not None:
            await psr.set_password(server, server_to_edit.password)
        if server_to_edit.panel_path is not None:
            await psr.set_panel_path(server, server_to_edit.panel_path)
        return {"message": "OK"}
