
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from shared.database import (
    session_manager,
)

from ..response import SuccessResponse
from ..schemas import (
    NewTicketSchema,
    TicketMessageCreateSchema,
    TicketSchema
)
from ..services import TicketService

router = APIRouter(prefix="/ticket", tags=["ticket"])


@router.post(
    path="/new_message/{ticket_id}",
    summary="Add a new message to an existing ticket"
)
async def new_message_ticket(ticket_id: UUID,
                             message: TicketMessageCreateSchema,
                             ticket_service: TicketService = Depends(
                                 TicketService.depends)
                             ) -> SuccessResponse:
    await ticket_service.new_message(ticket_id, message)
    return SuccessResponse()


@router.get(
    path="",
    summary="Get all feedback tickets"
)
async def get_all_tickets(ticket_service: TicketService = Depends(TicketService.depends)
                          ) -> list[TicketSchema]:
    return await ticket_service.all()


@router.get(
    path="/{ticket_id}",
    summary="Get an existing feedback ticket with its messages"
)
async def get_ticket(ticket_id: UUID,
                     ticket_service: TicketService = Depends(
                         TicketService.depends)
                     ) -> TicketSchema:
    return await ticket_service.get(ticket_id)


@router.patch(
    path="/close_ticket/{ticket_id}",
    summary="Close an existing feedback ticket"
)
async def close_ticket(ticket_id: UUID,
                       ticket_service: TicketService = Depends(
                           TicketService.depends)
                       ) -> SuccessResponse:
    await ticket_service.close(ticket_id)
    return SuccessResponse()
