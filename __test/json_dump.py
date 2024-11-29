


import json

from _3x_ui_.session_manager import parse_nested_json

obj = {
    "success": True,
    "msg": "Создать Успешно",
    "obj": {
        "id": 70,
        "up": 0,
        "down": 0,
        "total": 0,
        "remark": "",
        "enable": True,
        "expiryTime": 0,
        "clientStats": None,
        "listen": "",
        "port": 55184,
        "protocol": "socks",
        "settings": "{\n  \"auth\": \"password\",\n  \"accounts\": [\n    {\n      \"user\": \"Ym7ylmVX2M\",\n      \"pass\": \"CXtXDPVNlx\"\n    }\n  ],\n  \"udp\": true,\n  \"ip\": \"127.0.0.1\"\n}",
        "streamSettings": "",
        "tag": "inbound-55184",
        "sniffing": "{\n  \"enabled\": false,\n  \"destOverride\": [\n    \"http\",\n    \"tls\",\n    \"quic\",\n    \"fakedns\"\n  ],\n  \"metadataOnly\": false,\n  \"routeOnly\": false\n}",
        "allocate": "{\n  \"strategy\": \"always\",\n  \"refresh\": 5,\n  \"concurrency\": 3\n}"
    }
}



with open('__test/create_vpn/socks_response.json', mode='w') as file:
    json_str = json.dumps(obj=obj).replace('\\n', '').replace('\\"', '"').replace('"{', '{').replace('}"', '}')
    file.write(json_str)