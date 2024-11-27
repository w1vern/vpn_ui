


import json

from _3x_ui_.session_manager import parse_nested_json

obj = {
    "success": True,
    "msg": "Create Successfully",
    "obj": {
        "id": 36,
        "up": 0,
        "down": 0,
        "total": 0,
        "remark": "vless",
        "enable": True,
        "expiryTime": 0,
        "clientStats": None,
        "listen": "",
        "port": 56777,
        "protocol": "vless",
        "settings": "{\n  \"clients\": [\n    {\n      \"id\": \"61c1e56d-7204-4770-b34f-48f725d5c3ee\",\n      \"flow\": \"\",\n      \"email\": \"7uasrebw\",\n      \"limitIp\": 0,\n      \"totalGB\": 0,\n      \"expiryTime\": 0,\n      \"enable\": true,\n      \"tgId\": \"\",\n      \"subId\": \"wqxiphl006otd6pa\",\n      \"reset\": 0\n    }\n  ],\n  \"decryption\": \"none\",\n  \"fallbacks\": []\n}",
        "streamSettings": "{\n  \"network\": \"tcp\",\n  \"security\": \"none\",\n  \"externalProxy\": [],\n  \"tcpSettings\": {\n    \"acceptProxyProtocol\": false,\n    \"header\": {\n      \"type\": \"none\"\n    }\n  }\n}",
        "tag": "inbound-56777",
        "sniffing": "{\n  \"enabled\": false,\n  \"destOverride\": [\n    \"http\",\n    \"tls\",\n    \"quic\",\n    \"fakedns\"\n  ],\n  \"metadataOnly\": false,\n  \"routeOnly\": false\n}",
        "allocate": "{\n  \"strategy\": \"always\",\n  \"refresh\": 5,\n  \"concurrency\": 3\n}"
    }
}




with open('__test/create_vpn/vless_response.json', mode='w') as file:
    json_str = json.dumps(obj=obj).replace('\\n', '').replace('\\"', '"').replace('"{', '{').replace('}"', '}')
    file.write(json_str)