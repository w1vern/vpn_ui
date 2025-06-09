

import asyncio
from time import sleep

from services.infra._3x_ui_ import (PanelRepository, Service,
                                    server_session_manager)
from services.infra.database import (PanelServerRepository, ServerRepository,
                                     UserRepository, session_manager)
from services.infra.proxy_interface import AccessType


async def main():
    async with session_manager.context_session() as db_session:
        psr = PanelServerRepository(db_session)
        ur = UserRepository(db_session)
        server = (await psr.get_all())[0]
        user = (await ur.get_all())[0]
        async with server_session_manager.get_session(server) as server_session:
            service = Service(db_session, server_session)
            await service.get_config(user)
            await service.set_enable(user, False, AccessType.HTTP)
            sleep(5)
            await service.set_enable(user, True, AccessType.HTTP)

if __name__ == "__main__":
    asyncio.run(main())
