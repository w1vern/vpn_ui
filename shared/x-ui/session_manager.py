
import contextlib
import json
from collections.abc import AsyncIterator
from typing import Any
from uuid import UUID

import httpx

from shared.database import Server

from .exceptions import UnauthorizedException


class ServerSession():
    def __init__(
        self,
        server: Server,
        client: httpx.AsyncClient
    ) -> None:
        self.server = server
        self.client = client

    async def __make_request(
        self,
        path: str,
        method: str,
        body: dict[str, Any] | None = None
    ) -> httpx.Response:
        if not await self.__is_auth():
            await self.__auth()
        response = await self.client.request(method=method,
                                             url=self.__get_api_path(path),
                                             headers={
                                                 "Content-Type": "application/json"},
                                             json=body)
        return response

    def __get_api_path(
        self,
        endpoint: str
    ) -> str:
        return self.server.panel_url + "panel/api/inbounds/" + endpoint

    async def __is_auth(self) -> bool:
        response = await self.client.get(self.__get_api_path("list"))
        if response.status_code == 200:
            return True
        return False

    async def __auth(
        self
    ) -> None:
        resp = await self.client.post(
            self.server.panel_url + "login",
            json={"username": self.server.panel_login, "password": self.server.panel_password})
        resp.raise_for_status()

    async def __get_dict(
        self,
        response: httpx.Response
    ) -> dict[str, Any]:
        if response.status_code == 404:
            raise UnauthorizedException()
        return json.loads(response.text
                          .replace('\\n', '')
                          .replace('\\"', '"')
                          .replace('"{', '{')
                          .replace('}"', '}'))

    async def post(
        self,
        path: str,
        body: dict[str, Any] = {}
    ) -> httpx.Response:
        return await self.__make_request(path, "POST", body)

    async def get(
        self,
        path: str
    ) -> httpx.Response:
        return await self.__make_request(path, "GET")

    async def post_dict(
        self,
        path: str,
        body: dict[str, Any] = {}
    ) -> dict[str, object]:
        response = await self.post(path, body)
        return await self.__get_dict(response)

    async def get_dict(
        self,
        path: str
    ) -> dict[str, Any]:
        return await self.__get_dict(await self.get(path))


class ServerSessionManager:
    def __init__(
        self
    ) -> None:
        self.cookies: dict[UUID, httpx.Cookies] = {}

    @contextlib.asynccontextmanager
    async def get_session(
        self,
        server: Server
    ) -> AsyncIterator[ServerSession]:
        async with httpx.AsyncClient() as client:
            client.cookies = self.cookies.get(
                server.id,
                {}
            )
            yield ServerSession(server, client)
            self.cookies[server.id] = client.cookies


server_session_manager = ServerSessionManager()
