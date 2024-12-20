import uuid

from fastapi import Depends, HTTPException
from fastapi_controllers import Controller, delete, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from back.get_auth import get_user
from back.schemas.server import ServerToCreateScheme
from back.schemas.ticket import NewTicket, TicketMessage
from database.database import get_db_session
from database.models.user import User
from database.repositories.server_repository import ServerRepository


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
    async def create_new_ticket(self, new_ticket: NewTicket, user: User = Depends(get_user)):
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
    async def new_message_ticket(self, message: TicketMessage, user: User = Depends(get_user)):
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
    async def close_ticket(self, user: User = Depends(get_user)):
        pass
