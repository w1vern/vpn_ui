

import contextlib
import json
from typing import Any, AsyncIterator, Optional
import uuid
import httpx

from database.models import Server


def parse_nested_json(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str):
                try:
                    obj[key] = json.loads(value)
                except json.JSONDecodeError:
                    pass
            else:
                parse_nested_json(value)
    elif isinstance(obj, list):
        for item in obj:
            parse_nested_json(item)


class ServerSession():
    def __init__(self, server: Server, client: httpx.AsyncClient) -> None:
        self.server = server
        self.client = client

    async def __make_request(self, path: str, method: str, body: Optional[dict[str, Any]] = None) -> httpx.Response:
        if not await self.__is_auth():
            await self.__auth()
        return await self.client.request(method=method,
                                         url=self.__get_api_path(path),
                                         headers={
                                             "Content-Type": "application/json"},
                                         json=body)

    def __get_api_path(self, endpoint: str):
        return self.server.connection_string + "panel/api/inbounds/" + endpoint

    async def __is_auth(self) -> bool:
        response = await self.client.get(self.__get_api_path("list"))
        if response.status_code == 200:
            return True
        return False

    async def __auth(self) -> None:
        resp = await self.client.post(
            self.server.connection_string + "login",
            json={"username": self.server.login, "password": self.server.password})
        resp.raise_for_status()

    async def __get_dict(self, response: httpx.Response) -> dict[str, Any]:
        return json.loads(response.text.replace('\\n', '').replace('\\"', '"').replace('"{', '{').replace('}"', '}'))

    async def post(self, path: str, body: dict[str, Any]) -> httpx.Response:
        return await self.__make_request(path, "POST", body)

    async def get(self, path: str) -> httpx.Response:
        return await self.__make_request(path, "GET")

    async def post_dict(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        return await self.__get_dict(await self.post(path, body))

    async def get_dict(self, path: str) -> dict[str, Any]:
        return await self.__get_dict(await self.get(path))

    async def get_free_port(self) -> int:
        resp = await self.client.get(url=f"http://{self.server.ip}:9101/api/")
        return int(resp.text)


class ServerSessionManager:
    def __init__(self):
        self.cookies: dict[uuid.UUID, Any] = {}

    @contextlib.asynccontextmanager
    async def get_session(self, server: Server) -> AsyncIterator[ServerSession]:
        async with httpx.AsyncClient() as client:
            client.cookies = self.cookies.get(
                server.id, {})
            yield ServerSession(server, client)
            self.cookies[server.id] = client.cookies


server_session_manager = ServerSessionManager()
