from fastapi import APIRouter, Depends

from shared.infrastructure import NotificationToTG

from ..response import SuccessResponse
from ..services import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post(
    path="",
    summary="Create new notification",
    description='scheme like: {"en": "text", "ru": "Текст"}'
)
async def create(
    notification: NotificationToTG,
    notification_service: NotificationService = Depends(
        NotificationService.depends)
) -> SuccessResponse:
    await notification_service.send(notification)
    return SuccessResponse()
