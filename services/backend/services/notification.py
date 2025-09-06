



from fastapi import Depends

from .depends import get_user

from ..schemas import UserSchema

from ..rabbit import get_broker
from ..schemas import Notification
from faststream.rabbit import RabbitBroker



class NotificationService:
    def __init__(self,
                 broker: RabbitBroker,
                 user_schema: UserSchema
                 ) -> None:
        self.user_schema = user_schema
        self.broker = broker

    @classmethod
    async def depends(cls,
                      broker: RabbitBroker = Depends(get_broker),
                      user_schema: UserSchema = Depends(get_user)   
                      ) -> 'NotificationService':
        return cls(broker, user_schema)
    
    async def send(self, notification: Notification) -> None:
        pass