

import json
import random
import secrets
import string
import uuid
from typing import Any, Optional
from urllib import response

from httpx import get

from _3x_ui_.models import ProxyInbound, ProxyType, VpnInbound, VpnType
from _3x_ui_.session_manager import server_session_manager
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


def generate_sub_id(length: int = 16) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_short_ids(count: int = 8) -> list[str]:
    res = []
    for i in range(count):
        length = random.randint(2, 16)
        res.append(
            hex(random.randint(0b1 << 4 * (length-1), 0b1 << 4 * length))[2:])
    return res


async def create_proxy(server: Server, user: User, login: str | None = None, password: str | None = None, proxy_type: ProxyType = ProxyType.HTTP) -> Optional[ProxyInbound]:
    if login is None:
        login = secrets.token_urlsafe(8)
    if password is None:
        password = secrets.token_urlsafe(8)
    async with server_session_manager.get_session(server) as session, session_manager.session() as db_session:
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
        sur = ServerUserRepository(db_session)
        connections = await sur.get_by_id(server.id, user.id)
        params = dict()
        params[proxy_type.value] = response['obj']['id']
        if connections is None:
            connections = sur.create(
                server, user, **params)
            await db_session.commit()
        else:
            params[ProxyType.HTTP.value] = connections.http_id
            params[ProxyType.SOCKS.value] = connections.socks_id
            params[proxy_type.value] = response['obj']['id']
            await sur.update_ids(server, user, **params, vless_id=connections.vless_id, vless_reality_id=connections.vless_reality_id, vmess_id=connections.vmess_id)
            await db_session.commit()
        return ProxyInbound(server.ip, response['obj']['port'],
                            response['obj']['settings']['accounts'][0]['user'],
                            response['obj']['settings']['accounts'][0]['pass'])


async def create_vpn(server: Server, user: User, vpn_type: VpnType) -> bool:
    async with server_session_manager.get_session(server) as server_session, session_manager.session() as db_session:
        port = await server_session.get_free_port()
        settings = {**GlobalSettings.settings, **{
            "clients": [
                # {
                #     "id": str(uuid.uuid4()),
                #     "flow": "",
                #     "email": f"{user.telegram_username}-vless",
                #     "limitIp": 0,
                #     "totalGB": 0,
                #     "expiryTime": 0,
                #     "enable": True,
                #     "tgId": str(user.telegram_id),
                #     "subId": generate_sub_id(),
                #     "reset": 0
                # }
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
                    "shortIds": generate_short_ids(),
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
        await sr.update_vpn_ids(server, **params)
        await db_session.commit()
        return True


async def create_vpn_user(server: Server, user: User, vpn_type: VpnType):
    async with server_session_manager.get_session(server) as server_session, session_manager.session() as db_session:
        pass