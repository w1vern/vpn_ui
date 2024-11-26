

import asyncio
import json

from _3x_ui_.handlers import create_proxy, create_vpn
from _3x_ui_.models import ProxyType, VpnType
from _3x_ui_.session_manager import server_session_manager
from __test.test import server, user
from database.repositories.server_repository import ServerRepository


async def main():
    #await create_proxy(server, user)
    #await create_proxy(server, user, login="test", password="test", proxy_type=ProxyType.SOCKS5)    
    await create_vpn(server, user, VpnType.VLESS)



if __name__ == "__main__":
    asyncio.run(main())
