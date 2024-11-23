

import secrets
from typing import Any
from _3x_ui_.models import ProxyInbound, ProxyType
from database.models.server import Server
from database.models.user import User
from _3x_ui_.session_manager import server_session_manager
import json


async def create_proxy(server: Server, user: User, username: str = secrets.token_urlsafe(8), password: str = secrets.token_urlsafe(8), proxy_type: ProxyType = ProxyType.HTTP) -> ProxyInbound:
    async with server_session_manager.get_session(server) as session:
        port = await session.get_free_port()
        settings : dict[str, Any]= {
            "accounts":[{
            "user": username,
            "pass": password
            }],
            "allowTransparent": False
        }
        streamSettings = {
            
        }
        sniffing : dict[str, Any]= {
            "enabled": True,
            "destOverride": [
                "http",
                "tls",
                "quic",
                "fakedns"
            ],
            "metadataOnly": False,
            "routeOnly": False
        }
        allocate : dict[str, Any]= {
            "strategy": "always",
            "refresh": 5,
            "concurrency": 3
        }
        data : dict[str, Any]={
            "up": 0,
            "down": 0,
            "total": 0,
            "remark": f"{server.country_code}-{server.display_name}-{proxy_type.value}-{user.telegram_username}",
            "enable": True,
            "expiryTime": 0,
            "listen": "",
            "port": port,
            "protocol": proxy_type.value,
            "settings": json.dumps(settings),
            "streamSettings": json.dumps(streamSettings),
            "sniffing": json.dumps(sniffing),
            "allocate": json.dumps(allocate)
        }
        response = await session.post("add", body=data)
        print(response.status_code)
        print(response.text)
        pass