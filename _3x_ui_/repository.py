

import json
import random
import re
import secrets
import string
from time import process_time
import uuid
from typing import Any, Optional
from urllib import response

from click import Option
from fastapi import params
from httpx import get
import sniffio

from services.proxy_models import ProxyInbound, ProxyType, RealityOptions, VpnInbound, VpnType
from _3x_ui_.session_manager import ServerSession, server_session_manager
from database.models.server import Server
from database.models.user import User
from database.database import session_manager
from database.repositories.server_repository import ServerRepository
from database.repositories.server_user_repository import ServerUserRepository


class GlobalSettings:
    sniffing = {
        "enabled": False,
        "destOverride": [
            "http",
            "tls",
            "quic",
            "fakedns"
        ],
        "metadataOnly": False,
        "routeOnly": False
    }

    allocate = {
        "strategy": "always",
        "refresh": 5,
        "concurrency": 3
    }

    settings = {

    }

    streamSettings = {

    }

    data = {
        "up": 0,
        "down": 0,
        "total": 0,
        "enable": True,
        "expiryTime": 0,
        "listen": ""
    }


class PanelRepository:
    def __init__(self, server_session: ServerSession) -> None:
        self.server_session = server_session

    async def get_free_port(self) -> int:
        resp = await self.server_session.client.get(url=f"http://{self.server_session.server.ip}:9101/api/")
        return int(resp.text)

    async def create_proxy(self, login: str, password: str, port: int, user: User, proxy_type: ProxyType = ProxyType.HTTP) -> dict[str, Any]:
        settings = {**GlobalSettings.settings, **{
            "accounts": [{
                "user": login,
                "pass": password
            }],
            "allowTransparent": False
        }}
        streamSettings = {
            **GlobalSettings.streamSettings,
            **{}
        }
        sniffing = {**GlobalSettings.sniffing, **{}}
        allocate = {**GlobalSettings.allocate, **{}}

        data = {**GlobalSettings.data, **{
            "remark": f"{proxy_type.value[:-3]}-{self.server_session.server.country_code}-{user.telegram_username}",
            "port": port,
            "protocol": proxy_type.value[:-3],
            "settings": json.dumps(settings),
            "streamSettings": json.dumps(streamSettings),
            "sniffing": json.dumps(sniffing),
            "allocate": json.dumps(allocate)
        }}
        return await self.server_session.post_dict("add", body=data)

    async def create_vpn(self, user: User, sub_id: str, short_ids: list[str], vpn_type: VpnType = VpnType.VLESS) -> dict[str, Any]:
        async with server_session_manager.get_session(self.server_session.server) as server_session, \
                session_manager.session() as db_session:
            port = await self.get_free_port()
            uuid4 = uuid.uuid4()
            security = "none"
            protocol = "vless"
            
            settings = {**GlobalSettings.settings, **{
                "clients": [
                    {
                        "id": str(uuid.uuid4()),
                        "flow": "",
                        "email": f"{user.telegram_username}-{vpn_type.value[:-3]}-{uuid.uuid4()}",
                        "limitIp": 0,
                        "totalGB": 0,
                        "expiryTime": 0,
                        "enable": True,
                        "tgId": str(user.telegram_id),
                        "subId": sub_id,
                        "reset": 0
                    }
                ],
                "decryption": "none",
                "fallbacks": []
            }}

            streamSettings = {
                **GlobalSettings.streamSettings,
                **{
                    "network": "tcp",
                    "security": security,
                    "externalProxy": [],
                    "realitySettings": {
                        "show": False,
                        "xver": 0,
                        "dest": "yahoo.com:443",
                        "serverNames": ["yahoo.com", "www.yahoo.com"],
                        "privateKey": "",
                        "minClient": "",
                        "maxClient": "",
                        "maxTimediff": 0,
                        "shortIds": short_ids,
                        "settings": {
                            "publicKey": "",
                            "fingerprint": "random",
                            "serverName": "",
                            "spiderX": "/"
                        }
                    },
                    "tcpSettings": {
                        "acceptProxyProtocol": False,
                        "header": {
                            "type": "http",
                            "request": {
                                "version": "1.1",
                                "method": "GET",
                                "path": ["/"],
                                "headers": {}
                            },
                            "response": {
                                "version": "1.1",
                                "status": "200",
                                "reason": "OK",
                                "headers": {}
                            }
                        }
                    }

                }

            }

            sniffing = {**GlobalSettings.sniffing, **{}}
            allocate = {**GlobalSettings.allocate, **{}}
            data = {**GlobalSettings.data, **{
                "remark": f"{server.country_code}-{server.display_name}-{vpn_type.value[:-3]}-{user.telegram_username}",
                "port": port,
                "protocol": "vless",
                "settings": json.dumps(settings),
                "streamSettings": json.dumps(streamSettings),
                "sniffing": json.dumps(sniffing),
                "allocate": json.dumps(allocate)
            }}
            response = await server_session.post_dict("add", body=data)
            with open("__test/vless_create_response.json", "w") as f:
                json.dump(response, f, indent=4)
            if response['success'] is False:
                return False
            print('hello mather fucker')
            sr = ServerRepository(db_session)
            params = dict()
            params[VpnType.VLESS.value] = server.vless_id
            params[VpnType.VLESS_REALITY.value] = server.vless_reality_id
            params[VpnType.VMESS.value] = server.vmess_id
            params[vpn_type.value] = response['obj']['id']
            print(response['obj']['id'])
            print(params)
            await sr.update_vpn_ids(server, **params)
            return True

    async def create_vpn_user(server: Server, user: User, vpn_type: VpnType) -> Optional[VpnInbound]:
        async with server_session_manager.get_session(server) as server_session, \
                session_manager.session() as db_session:
            sur = ServerUserRepository(db_session)
            sr = ServerRepository(db_session)
            if getattr(server, vpn_type.value) == 0:
                await create_vpn(server, user, vpn_type)
                tmp_server = await sr.get_by_id(server.id)
                if tmp_server is None:
                    return
                server = tmp_server
            uuid4 = uuid.uuid4()
            connections = await sur.get_by_id(server.id, user.id)
            if connections is None:
                connections = await sur.create(server, user)
                if connections is None:
                    return None
            response = await server_session.post_dict(path='addClient', body={
                "id": getattr(server, vpn_type.value),
                "settings": json.dumps({
                    "clients": [{
                        "id": str(uuid4),
                        "flow": "",
                        "email": f"{server.country_code}-{user.telegram_username}-{vpn_type.value}",
                        "limitIp": 0,
                        "totalGB": 0,
                        "expiryTime": 0,
                        "enable": True,
                        "tgId": str(user.telegram_id),
                        "subId": generate_sub_id(),
                        "reset": 0
                    }],
                    "decryption": "none",
                    "fallbacks": []
                })
            })
            if response['success'] is False:
                print(response['msg'])
                return None
            params = dict()
            params[VpnType.VLESS.value] = connections.vless_id
            params[VpnType.VLESS_REALITY.value] = connections.vless_reality_id
            params[VpnType.VMESS.value] = connections.vmess_id
            params[vpn_type.value] = uuid4
            await sur.update_ids(server, user, **params, http_id=connections.http_id, socks_id=connections.socks_id)
            inbound = await server_session.get(path=f'get/{uuid4}')
            print(inbound.text)
            pass
