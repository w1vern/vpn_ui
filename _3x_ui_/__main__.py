

import asyncio
from urllib import response
from _3x_ui_.handlers import create_proxy, create_vless
from _3x_ui_.models import ProxyType
from _3x_ui_.session_manager import server_session_manager
from database.repositories.server_repository import ServerRepository
import json

from __test.test import server, user





async def main():
    
    await create_vless(server, user)    



if __name__ == "__main__":
    asyncio.run(main())
