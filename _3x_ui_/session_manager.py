

import contextlib
from typing import AsyncIterator
import httpx

from sqlalchemy import Boolean
from database.models import Server


class ServerSession():
    def __init__(self, server: Server, client: httpx.AsyncClient) -> None:
        self.server = server
        self.client = client

    async def __make_request(self, path: str, method: str) -> httpx.Response:
        if not await self.__is_auth():
            await self.__auth()
        return await self.client.request(method=method,
                                         url=self.__get_api_path(path),
                                         headers={
                                             "Content-Type": "application/json"})

    def __get_api_path(self, endpoint: str):
        return self.server.connection_string + "panel/api/inbounds/" + endpoint

    async def __is_auth(self) -> Boolean:
        response = await self.client.get(self.__get_api_path("list"))
        if response.status_code == 200:
            return True
        return False

    async def __auth(self) -> None:
        resp = await self.client.post(
            self.server.connection_string + "login",
            json={"username": self.server.login, "password": self.server.password})
        resp.raise_for_status()

    async def post(self, path: str) -> httpx.Response:
        return await self.__make_request(path, "POST")

    async def get(self, path: str) -> httpx.Response:
        return await self.__make_request(path, "GET")


class ServerSessionManager:
    def __init__(self):
        self.cookies = {}

    @contextlib.asynccontextmanager
    async def get_session(self, server: Server) -> AsyncIterator[ServerSession]:
        async with httpx.AsyncClient() as client:
            client.cookies = self.cookies.get(server.id, {})
            yield ServerSession(server, client)
            self.cookies[server.id] = client.cookies


server_session_manager = ServerSessionManager()
