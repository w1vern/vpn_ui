

import asyncio
from urllib import response
from _3x_ui_.handlers import create_proxy
from _3x_ui_.models import ProxyType
from _3x_ui_.session_manager import server_session_manager
from database.repositories.server_repository import ServerRepository
import json

from test import server, user





async def main():
    
    #async with server_session_manager.get_session(server) as session:
        #response = await session.get_dict("list")
        #with open("test.json", "w") as f:
        #    json.dump(response, f, indent=4)
        #print(await session.get_free_port())
        #print(json.dumps(response, indent=4))
    pass



if __name__ == "__main__":
    asyncio.run(main())
