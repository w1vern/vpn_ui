

import asyncio
from time import sleep

from shared.database import (
    PanelServerRepository,
    ServerRepository,
    UserRepository,
    session_manager,
)
from shared.proxy_interface import (
    AccessType,
)

from ..repository import PanelRepository
from ..service import Service
from ..session_manager import server_session_manager


async def main():
    async with session_manager.context_session() as db_session:
        psr = PanelServerRepository(db_session)
        ur = UserRepository(db_session)
        server = (await psr.get_all())[0]
        user = (await ur.get_all())[0]
        async with server_session_manager.get_session(server) as server_session:
            service = Service(db_session, server_session)
            config = await service.get_config(user, AccessType.VLESS_REALITY, create_if_not_exists=True)

if __name__ == "__main__":
    asyncio.run(main())
