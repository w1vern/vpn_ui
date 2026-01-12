
from fastapi import Depends
from faststream.rabbit import RabbitBroker

from shared.infrastructure import NotificationToTG

from ..depends import get_user
from ..rabbit import get_broker, send_tg_notification
from ..schemas import UserSchema


class NotificationService:
    def __init__(
        self,
        broker: RabbitBroker,
        user_schema: UserSchema
    ) -> None:
        self.user_schema = user_schema
        self.broker = broker

    @classmethod
    async def depends(
        cls,
        broker: RabbitBroker = Depends(get_broker),
        user_schema: UserSchema = Depends(get_user)
    ) -> 'NotificationService':
        return cls(broker, user_schema)

    async def send(
        self,
        notification: NotificationToTG
    ) -> None:
        await send_tg_notification(notification, self.broker)
