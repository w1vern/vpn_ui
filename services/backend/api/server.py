

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (PanelServerRepository, ServerRepository,
                             session_manager)

from ..get_auth import get_user
from ..schemas import (EditServerSchema, ServerSchema, ServerToCreateSchema,
                       UserSchema)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/get_all")
async def get_all(user: UserSchema = Depends(get_user),
                  session: AsyncSession = Depends(session_manager.session)
                  ) -> list[ServerSchema]:
    if user.rights.is_control_panel_user is False:
        raise HTTPException(
            status_code=403, detail="user is not control panel member")
    psr = PanelServerRepository(session)
    servers = await psr.get_all()
    result = []
    for server in servers:
        server_to_send = ServerSchema(
            id=server.id,
            display_name=server.server.display_name,
            ip=server.server.ip,
            country_code=server.server.country_code,
            is_available=server.server.is_available,
            starting_date=server.server.starting_date.isoformat(),
            closing_date=server.server.closing_date.isoformat(),
            panel_path=server.panel_path,
            login=server.login,
            password=server.password
        )
        result.append(server_to_send)
    return result


@router.post("/create",
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
async def create_server(server_to_create: ServerToCreateSchema,
                        user: UserSchema = Depends(get_user),
                        session: AsyncSession = Depends(
                            session_manager.session)
                        ):
    if user.rights.is_control_panel_user is False:
        raise HTTPException(
            status_code=403, detail="user is not control panel member")
    if user.rights.is_server_editor is False:
        raise HTTPException(
            status_code=403, detail="user is not server editor")
    sr = ServerRepository(session)
    psr = PanelServerRepository(session)
    server = await sr.create(ip=server_to_create.ip,
                             country_code=server_to_create.country_code,
                             is_available=server_to_create.is_available,
                             display_name=server_to_create.display_name,
                             starting_date=datetime.fromisoformat(
                                 server_to_create.starting_date),
                             closing_date=datetime.fromisoformat(
                                 server_to_create.closing_date))
    pserver = await psr.create(server=server,
                               login=server_to_create.login,
                               password=server_to_create.password,
                               panel_path=server_to_create.panel_path)
    if not (server and pserver):
        raise HTTPException(status_code=400, detail="Server create error")
    return {"message": "OK"}


@router.post("/edit",
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
async def edit_server(server_to_edit: EditServerSchema,
                      user: UserSchema = Depends(get_user),
                      session: AsyncSession = Depends(session_manager.session)
                      ):
    if user.rights.is_control_panel_user is False:
        raise HTTPException(
            status_code=403, detail="user is not control panel member")
    if user.rights.is_server_editor is False:
        raise HTTPException(
            status_code=403, detail="user is not server editor")
    sr = ServerRepository(session)
    psr = PanelServerRepository(session)
    server = await sr.get_by_id(server_to_edit.id)
    pserver = await psr.get_by_id(server_to_edit.id)
    if not (server and pserver):
        raise HTTPException(status_code=404, detail="Server not found")
    if server_to_edit.ip is not None:
        await sr.set_ip(server, server_to_edit.ip)
    if server_to_edit.country_code is not None:
        await sr.set_country_code(server, server_to_edit.country_code)
    if server_to_edit.display_name is not None:
        await sr.set_display_name(server, server_to_edit.display_name)
    if server_to_edit.created_date is not None:
        await sr.set_created_date(server, datetime.fromisoformat(server_to_edit.created_date))
    if server_to_edit.closing_date is not None:
        await sr.set_closing_date(server, datetime.fromisoformat(server_to_edit.closing_date))
    if server_to_edit.is_available is not None:
        await sr.set_is_available(server, server_to_edit.is_available)
    if server_to_edit.login is not None:
        await psr.set_login(pserver, server_to_edit.login)
    if server_to_edit.password is not None:
        await psr.set_password(pserver, server_to_edit.password)
    if server_to_edit.panel_path is not None:
        await psr.set_panel_path(pserver, server_to_edit.panel_path)
    return {"message": "OK"}
