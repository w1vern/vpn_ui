

import uuid

from fastapi import Depends, HTTPException
from fastapi_controllers import Controller, delete, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from back.get_auth import get_user
from back.schemas.server_scheme import ServerToCreate
from database.database import get_db_session
from database.models.user import User
from database.repositories.server_repository import ServerRepository


class ServerController(Controller):
    prefix = "/server"
    tags = ["server"]

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    @post(
        "/create",
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
    async def create_server(self, server: ServerToCreate, user: User = Depends(get_user)):
        pass

    @post(
        "/update",
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
    async def update_server(self, server: ServerToCreate, user: User = Depends(get_user)):
        pass

    @post(
        "/deactivate",
        summary="Deactivate a server",
        description=(
            "This endpoint allows the user to deactivate an existing server by its ID. "
            "The server ID must be provided as a parameter."
        ),
        responses={
            200: {"description": "Server successfully deactivated"},
            401: {"description": "Unauthorized user"},
            404: {"description": "Server not found"},
        },
    )
    async def deactivate_server(self, server_id: uuid.UUID, user: User = Depends(get_user)):
        pass