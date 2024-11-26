

from enum import Enum
from tkinter import E
from typing import Optional


class ProxyType(str, Enum):
    HTTP = "http_id"
    SOCKS = "socks_id"

class VpnType(str, Enum):
    VLESS = "vless_id"
    VLESS_REALITY = "vless_reality_id"
    VMESS = "vmess_id"



class ProxyInbound:
    def __init__(self, ip: str, port: int, login: str, password: str):
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

    


class Security:
    def create_string(self) -> str:
        return 'none'


class RealityOptions(Security):
    def __init__(self, public_key: str, fp: str, server_name_indication: str, sid: str, spx: str):
        self.security_name = "reality"
        self.public_key = public_key
        self.fp = fp
        self.server_name_indication = server_name_indication
        self.sid = sid
        self.spx = spx

    def create_string(self) -> str:
        return f"{self.security_name}&pbk={self.public_key}&fp={self.fp}&sni={self.server_name_indication}&sid={self.sid}&spx={self.spx}"


class VpnInbound:
    def __init__(self, uuid: str, ip: str, port: int, protocol: str, path: str, header_type:str = "", security: Security = Security(), remark: str = ""):
        self.uuid = uuid
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.path = path
        self.header_type = header_type
        self.security = security
        self.remark = remark

    def create_string(self):
        return f"vless://{self.uuid}@{self.ip}:{self.port}?type={self.protocol}&path={self.path}&headerType={self.header_type}&security={self.security.create_string()}#{self.remark}"
