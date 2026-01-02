
from uuid import UUID

from fastapi import APIRouter, Depends

from ..response import SuccessResponse
from ..schemas import (
    TicketMessageCreateSchema,
    TicketMessageSchema,
    TicketSchema
)
from ..services import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post(
    path="/{ticket_id}/messages",
    summary="Add a new message to an existing ticket"
)
async def new_message_ticket(
    ticket_id: UUID,
    message: TicketMessageCreateSchema,
    ticket_service: TicketService = Depends(
        TicketService.depends)
) -> TicketMessageSchema:
    return await ticket_service.new_message(ticket_id, message)


@router.get(
    path="",
    summary="Get all feedback tickets"
)
async def get_all_tickets(
    ticket_service: TicketService = Depends(TicketService.depends)
) -> list[TicketSchema]:
    return await ticket_service.all()


@router.get(
    path="/{ticket_id}",
    summary="Get an existing feedback ticket with its messages"
)
async def get_ticket(
    ticket_id: UUID,
    ticket_service: TicketService = Depends(
        TicketService.depends)
) -> TicketSchema:
    return await ticket_service.get(ticket_id)


@router.patch(
    path="/{ticket_id}/close",
    summary="Close an existing feedback ticket"
)
async def close_ticket(
    ticket_id: UUID,
    ticket_service: TicketService = Depends(
        TicketService.depends)
) -> SuccessResponse:
    await ticket_service.close(ticket_id)
    return SuccessResponse()
