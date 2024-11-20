

import asyncio
from _3x_ui_.session_manager import server_session_manager
import httpx
from database.repositories.server_repository import ServerRepository
import json

from test import server

async def main():
    
    async with server_session_manager.get_session(server) as session:
        resp = await session.get("list")
        users = json.loads(resp.text)
        print(users)



if __name__ == "__main__":
    asyncio.run(main())
