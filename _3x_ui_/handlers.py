

import secrets
from typing import Any, Optional
from urllib import response
import uuid
from _3x_ui_.models import ProxyInbound, ProxyType, VpnInbound
from database.models.server import Server
from database.models.user import User
from _3x_ui_.session_manager import server_session_manager
import json


class GlobalSettings:
    sniffing = {
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


async def create_proxy(server: Server, user: User, login: str | None = None, password: str | None = None, proxy_type: ProxyType = ProxyType.HTTP) -> Optional[ProxyInbound]:
    if login is None:
        login = secrets.token_urlsafe(8)
    if password is None:
        password = secrets.token_urlsafe(8)
    async with server_session_manager.get_session(server) as session:
        port = await session.get_free_port()
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
            "remark": f"{server.country_code}-{server.display_name}-{proxy_type.value}-{user.telegram_username}",
            "port": port,
            "protocol": proxy_type.value,
            "settings": json.dumps(settings),
            "streamSettings": json.dumps(streamSettings),
            "sniffing": json.dumps(sniffing),
            "allocate": json.dumps(allocate)
        }}
        response = await session.post_dict("add", body=data)
        if response['success'] is False:
            return None
        return ProxyInbound(server.ip, response['obj']['port'],
                            response['obj']['settings']['accounts'][0]['user'],
                            response['obj']['settings']['accounts'][0]['pass'])

async def create_vless(server: Server, user: User) -> bool:
    async with server_session_manager.get_session(server) as session:
        port = await session.get_free_port()
        settings = {**GlobalSettings.settings, **{
            "clients": [
                {
                    "id": str(uuid.uuid4()),
                    "flow": "",
                    "email": f"{user.telegram_username}-vless",
                    "limitIp": 0,
                    "totalGB": 0,
                    "expiryTime": 0,
                    "enable": True,
                    "tgId": str(user.telegram_id),
                    #"subId": "z34paw6akvter1p4",
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
                "security": "reality",
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
                    # "shortIds": [
                    #     "72cc863870",
                    #     "051007e8c5b0",
                    #     "24f0965625b1e0",
                    #     "31d8b34ed4bf563d",
                    #     "a16c84f7",
                    #     "11ab",
                    #     "63",
                    #     "71db02"
                    # ],
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
            "remark": f"{server.country_code}-{server.display_name}-vless",
            "port": port,
            "protocol": "vless",
            "settings": json.dumps(settings),
            "streamSettings": json.dumps(streamSettings),
            "sniffing": json.dumps(sniffing),
            "allocate": json.dumps(allocate)
        }}
        response = await session.post_dict("add", body=data)
        with open("__test/vless_create_response.json", "w") as f:
            json.dump(response, f, indent=4)
        if response['success'] is False:
            return False
        return True
    
async def create_vless_user(server: Server, user: User):
    async with server_session_manager.get_session(server) as session:
        pass