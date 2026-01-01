
import json
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from shared.database import ServerInbound, User
from shared.infrastructure import setup_logger

from .exceptions import (
    BaseXUIException,
    UndefinedException,
    UnexpectedFailureException
)
from .session_manager import ServerSession

logger = setup_logger(__name__)

P = ParamSpec('P')
T = TypeVar('T')


def handle_exceptions(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except BaseXUIException:
            raise
        except Exception as e:
            raise UndefinedException(str(e))
    return wrapper


class PanelRepository:
    def __init__(
        self,
        server_session: ServerSession
    ) -> None:
        self.server_session = server_session

    @handle_exceptions
    async def ensure_user_exists(
        self,
        *,
        user: User,
        server_inbound: ServerInbound
    ) -> None:
        if not await self.check_user_exists(user=user, server_inbound=server_inbound):
            await self.create_vless_user(user=user, server_inbound=server_inbound)

    @handle_exceptions
    async def check_user_exists(
        self,
        *,
        user: User,
        server_inbound: ServerInbound
    ) -> bool:
        response = await self.server_session.get_dict(
            path=f"getClientTraffics/{server_inbound.inbound_id}.{user.internal_id}")
        return response['success']

    @handle_exceptions
    async def create_vless_user(
        self,
        *,
        user: User,
        server_inbound: ServerInbound
    ) -> None:
        response = await self.server_session.post_dict(
            path='addClient',
            body={
                "id": server_inbound.inbound_id,
                "settings": json.dumps({
                    "clients": [{
                        "id": str(user.id),
                        "email": f"{server_inbound.inbound_id}.{user.internal_id}",
                    }]
                })
            })
        if response['success'] is False:
            raise UnexpectedFailureException()

    @handle_exceptions
    async def delete_vless_user(
        self,
        *,
        user: User,
        server_inbound: ServerInbound,
    ) -> None:
        response = await self.server_session.post_dict(
            path=f"{server_inbound.inbound_id}/delClientByEmail/{server_inbound.inbound_id}.{user.internal_id}"
        )
        if response['success'] is False:
            raise UnexpectedFailureException()

    @handle_exceptions
    async def get_user_traffic(
        self,
        *,
        user: User,
        server_inbound: ServerInbound
    ) -> int:
        response = await self.server_session.get_dict(
            path=f"getClientTraffics/{server_inbound.inbound_id}.{user.internal_id}")
        if response['success'] is False:
            raise UnexpectedFailureException()
        return response['obj']['up'] + response['obj']['down']

    @handle_exceptions
    async def reset_user_traffic(
        self,
        *,
        user: User,
        server_inbound: ServerInbound
    ) -> None:
        response = await self.server_session.post_dict(
            path=f"resetClientTraffic/{server_inbound.inbound_id}.{user.internal_id}")
        if response['success'] is False:
            raise UnexpectedFailureException()
