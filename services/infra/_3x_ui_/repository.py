

import json
import uuid
from typing import Any

from _3x_ui_.session_manager import ServerSession
from infra.database.models.user import User
from interfaces.proxy.models import ProxyType, VpnType


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
        "up": 500,
        "down": 300,
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

    async def create_proxy(self,
                           login: str,
                           password: str,
                           port: int,
                           proxy_type: ProxyType,
                           remark: str
                           ) -> dict[str, Any]:
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

    async def create_vpn(self,
                         user: User,
                         uuid4: uuid.UUID,
                         sub_id: str,
                         short_ids: list[str],
                         port: int,
                         vpn_type: VpnType,
                         email: str,
                         protocol: str,
                         remark: str,
                         public_key: str,
                         private_key: str
                         ) -> dict[str, Any]:
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
            "protocol": protocol,
            "settings": json.dumps(settings),
            "streamSettings": json.dumps(streamSettings),
            "sniffing": json.dumps(sniffing),
            "allocate": json.dumps(allocate)
        }}
        return await self.server_session.post_dict("add", body=data)

    async def create_vpn_user(self,
                              uuid4: uuid.UUID,
                              sub_id: str,
                              user: User,
                              vpn_type: VpnType,
                              email: str
                              ) -> dict[str, Any]:
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

    async def set_inbound_enabled(self,
                                  id: int,
                                  enable: bool
                                  ) -> dict[str, Any]:
        info = await self.server_session.get(path=f"get/{id}")
        info = json.loads(info.text)
        info = info["obj"]
        del (info["id"])
        info["enable"] = enable
        response = await self.server_session.post_dict(path=f"update/{id}", body=info)
        return response

    async def set_vpn_user_enabled(self,
                                   inbound_id: int,
                                   client_id: uuid.UUID,
                                   enable: bool
                                   ) -> dict[str, Any]:
        info = await self.get_inbound_info(inbound_id)
        data = None
        for client in info["obj"]["settings"]["clients"]:
            if client["id"] == str(client_id):
                data = client
                data["enable"] = enable
                break
        if data is None:
            return {}
        response = await self.server_session.post_dict(path=f"updateClient/{client_id}",
                                                       body={
            "id": inbound_id,
            "settings": json.dumps({
                "clients": [data]})})
        return response

    async def delete_inbound(self, id: int) -> dict[str, Any]:
        response = await self.server_session.post_dict(path=f"del/{id}")
        return response

    async def delete_vpn_user(self, inbound_id: int, client_id: uuid.UUID) -> dict[str, Any]:
        response = await self.server_session.post_dict(path=f"{inbound_id}/delClient/{client_id}")
        return response

    async def get_inbound_info(self, id: int) -> dict[str, Any]:
        response = await self.server_session.get_dict(path=f"get/{id}")
        return response

    async def get_vpn_user_traffic(self, email: str) -> dict[str, Any]:
        response = await self.server_session.get_dict(path=f"getClientTraffics/{email}")
        return response

    async def reset_proxy_traffic(self, id: int) -> dict[str, Any]:
        response = await self.server_session.post_dict(path=f"resetAllClientTraffics/{id}")
        return response

    async def reset_vpn_user_traffic(self, email: str) -> dict[str, Any]:
        response = await self.server_session.post_dict(path=f"resetClientTraffic/{email}")
        return response
