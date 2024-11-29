

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
from fastapi import params, security
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

    async def create_proxy(self, login: str, password: str, port: int, user: User, proxy_type: ProxyType, remark: str) -> dict[str, Any]:
        settings = {**GlobalSettings.settings, **{
            "accounts": [{
                "user": login,
                "pass": password
            }],
            "allowTransparent": False
        }}
        if proxy_type == ProxyType.SOCKS:
            settings["auth"] = "password"
            settings["udp"] = True
            settings["ip"] = "127.0.0.1"
        streamSettings = {
            **GlobalSettings.streamSettings,
            **{}
        }
        sniffing = {**GlobalSettings.sniffing, **{}}
        allocate = {**GlobalSettings.allocate, **{}}

        data = {**GlobalSettings.data, **{
            "remark": remark,
            "port": port,
            "protocol": proxy_type.value[:-3],
            "settings": json.dumps(settings),
            "streamSettings": json.dumps(streamSettings),
            "sniffing": json.dumps(sniffing),
            "allocate": json.dumps(allocate)
        }}
        return await self.server_session.post_dict("add", body=data)

    async def create_vpn(self, user: User, uuid4: uuid.UUID, sub_id: str, short_ids: list[str], port: int, vpn_type: VpnType, email: str, protocol: str, remark: str, public_key: str, private_key: str) -> dict[str, Any]:
        security = "none"
        if vpn_type == VpnType.VLESS_REALITY:
            security = "reality"

        settings = {**GlobalSettings.settings, **{
            "clients": [
                {
                    "id": str(uuid4),
                    "flow": "",
                    "email": email,
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
                    "privateKey": private_key,
                    "minClient": "",
                    "maxClient": "",
                    "maxTimediff": 0,
                    "shortIds": short_ids,
                    "settings": {
                        "publicKey": public_key,
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
            "remark": remark,
            "port": port,
            "protocol": "vless",
            "settings": json.dumps(settings),
            "streamSettings": json.dumps(streamSettings),
            "sniffing": json.dumps(sniffing),
            "allocate": json.dumps(allocate)
        }}
        return await self.server_session.post_dict("add", body=data)

    async def create_vpn_user(self, uuid4: uuid.UUID, sub_id: str, user: User, vpn_type: VpnType, email: str) -> dict[str, Any]:
        return await self.server_session.post_dict(path='addClient', body={
            "id": getattr(self.server_session.server, vpn_type.value),
            "settings": json.dumps({
                "clients": [{
                    "id": str(uuid4),
                    "flow": "",
                    "email": email,
                    "limitIp": 0,
                    "totalGB": 0,
                    "expiryTime": 0,
                    "enable": True,
                    "tgId": str(user.telegram_id),
                    "subId": sub_id,
                    "reset": 0
                }],
                "decryption": "none",
                "fallbacks": []
            })
        })
