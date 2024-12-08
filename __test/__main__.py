

import asyncio
import json
from operator import is_
import uuid

from _3x_ui_ import session_manager
from _3x_ui_.repository import PanelRepository
from _3x_ui_.service import Service
from database.repositories.panel_server_repository import PanelServerRepository
from interface.proxy.models import *
from _3x_ui_.session_manager import server_session_manager
# from __test.test import server, user
from database.repositories.server_repository import ServerRepository
from database.database import session_manager
from database.repositories.user_repository import UserRepository


async def main():
    async with session_manager.session() as db_session:
        psr = PanelServerRepository(db_session)
        ur = UserRepository(db_session)
        server = (await psr.get_all())[0]
        user = (await ur.get_all())[0]
        async with server_session_manager.get_session(server) as server_session:
            service = Service(db_session, server_session)
            await service.get_config(user)

if __name__ == "__main__":
    asyncio.run(main())
