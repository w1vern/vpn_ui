
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import session_manager

from ..get_auth import get_user
from ..schemas import (NewTicket, TicketMessage,
                       UserSchema)

router = APIRouter(prefix="/ticket", tags=["ticket"])


@router.post(
    path="",
    summary="Create a new feedback ticket"
)
async def create_new_ticket(new_ticket: NewTicket,
                            user: UserSchema = Depends(get_user),
                            session: AsyncSession = Depends(
                                session_manager.session)
                            ):
    pass


@router.post(
    path="/new_message",
    summary="Add a new message to an existing ticket"
)
async def new_message_ticket(message: TicketMessage,
                             user: UserSchema = Depends(get_user),
                             session: AsyncSession = Depends(
                                 session_manager.session)
                             ):
    pass


@router.patch(
    path="/close_ticket/{ticket_id}",
    summary="Close an existing feedback ticket"
)
async def close_ticket(user: UserSchema = Depends(get_user),
                       session: AsyncSession = Depends(session_manager.session)
                       ):
    pass
