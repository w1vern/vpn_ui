import uuid

from back.get_auth import get_user
from back.schemas.server import ServerToCreateSchema
from back.schemas.ticket import NewTicket, TicketMessage
from back.schemas.user import UserSchema
from fastapi import Depends, HTTPException
from fastapi_controllers import Controller, delete, get, post
from infra.database.main import get_db_session
from infra.database.models.user import User
from infra.database.repositories.server_repository import ServerRepository
from sqlalchemy.ext.asyncio import AsyncSession


class TicketController(Controller):
    prefix = "/feedback"
    tags = ["feedback"]

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    @post("/new_ticket",
          summary="Create a new feedback ticket",
          description=(
              "This endpoint allows the user to create a new feedback ticket. "
              "The ticket details are provided in the request body."
          ),
          responses={
              200: {"description": "Ticket successfully created"},
              401: {"description": "Unauthorized user"},
              400: {"description": "Invalid ticket data"},
          },
          )
    async def create_new_ticket(self, new_ticket: NewTicket, user: UserSchema = Depends(get_user)):
        pass

    @post("/new_message",
          summary="Add a message to an existing ticket",
          description=(
              "This endpoint allows the user to add a new message to an existing feedback ticket. "
              "The message details are provided in the request body."
          ),
          responses={
              200: {"description": "Message successfully added to the ticket"},
              401: {"description": "Unauthorized user"},
              404: {"description": "Ticket not found"},
          },
          )
    async def new_message_ticket(self, message: TicketMessage, user: UserSchema = Depends(get_user)):
        pass

    @post("/close_ticket",
          summary="Close an existing feedback ticket",
          description=(
              "This endpoint allows the user to close an existing feedback ticket. "
              "The user must have the necessary permissions to perform this action."
          ),
          responses={
              200: {"description": "Ticket successfully closed"},
              401: {"description": "Unauthorized user"},
              404: {"description": "Ticket not found"},
          },
          )
    async def close_ticket(self, user: UserSchema = Depends(get_user)):
        pass
