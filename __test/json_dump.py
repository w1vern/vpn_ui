


import asyncio
from http import server
import json
from _3x_ui_.session_manager import server_session_manager
from database.database import session_manager
from database.repositories.panel_server_repository import PanelServerRepository

obj = {
    "success": True,
    "msg": "Create Successfully",
    "obj": {
        "id": 78,
        "up": 0,
        "down": 0,
        "total": 0,
        "remark": "test_vless_reality",
        "enable": True,
        "expiryTime": 0,
        "clientStats": True,
        "listen": "",
        "port": 27222,
        "protocol": "vless",
        "settings": "{\n  \"clients\": [\n    {\n      \"id\": \"60f0d14c-99d3-4e0a-a716-82438f3f90c2\",\n      \"flow\": \"\",\n      \"email\": \"this_is_email\",\n      \"limitIp\": 0,\n      \"totalGB\": 0,\n      \"expiryTime\": 0,\n      \"enable\": true,\n      \"tgId\": \"\",\n      \"subId\": \"iv0e3zbdfba6vbpu\",\n      \"reset\": 0\n    }\n  ],\n  \"decryption\": \"none\",\n  \"fallbacks\": []\n}",
        "streamSettings": "{\n  \"network\": \"tcp\",\n  \"security\": \"reality\",\n  \"externalProxy\": [],\n  \"realitySettings\": {\n    \"show\": false,\n    \"xver\": 0,\n    \"dest\": \"yahoo.com:443\",\n    \"serverNames\": [\n      \"yahoo.com\",\n      \"www.yahoo.com\"\n    ],\n    \"privateKey\": \"\",\n    \"minClient\": \"\",\n    \"maxClient\": \"\",\n    \"maxTimediff\": 0,\n    \"shortIds\": [\n      \"eff76f\",\n      \"58\",\n      \"a242\",\n      \"20baee5004d58ca8\",\n      \"e8517423c5c358\",\n      \"226b2063660c\",\n      \"6264c19396\",\n      \"4e43ed5b\"\n    ],\n    \"settings\": {\n      \"publicKey\": \"\",\n      \"fingerprint\": \"random\",\n      \"serverName\": \"\",\n      \"spiderX\": \"/\"\n    }\n  },\n  \"tcpSettings\": {\n    \"acceptProxyProtocol\": false,\n    \"header\": {\n      \"type\": \"http\",\n      \"request\": {\n        \"version\": \"1.1\",\n        \"method\": \"GET\",\n        \"path\": [\n          \"/\"\n        ],\n        \"headers\": {}\n      },\n      \"response\": {\n        \"version\": \"1.1\",\n        \"status\": \"200\",\n        \"reason\": \"OK\",\n        \"headers\": {}\n      }\n    }\n  }\n}",
        "tag": "inbound-27222",
        "sniffing": "{\n  \"enabled\": false,\n  \"destOverride\": [\n    \"http\",\n    \"tls\",\n    \"quic\",\n    \"fakedns\"\n  ],\n  \"metadataOnly\": false,\n  \"routeOnly\": false\n}",
        "allocate": "{\n  \"strategy\": \"always\",\n  \"refresh\": 5,\n  \"concurrency\": 3\n}"
    }
}

async def main():
    async with session_manager.session() as session:
        psr = PanelServerRepository(session)
        server = (await psr.get_all())[0]
    async with server_session_manager.get_session(server) as server_session:
        dict = await server_session.get_dict(path='list')
    with open('__test/json/list.json', mode='w') as file:
        json.dump(dict, file, indent=4)


if __name__ == "__main__":
    asyncio.run(main())