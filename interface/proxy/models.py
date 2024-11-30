

import datetime
from enum import Enum
from re import A


class AccessType(str, Enum):
    pass


class ProxyType(AccessType):
    HTTP = "http_id"
    SOCKS = "socks_id"


class VpnType(AccessType):
    VLESS = "vless_id"
    VLESS_REALITY = "vless_reality_id"
    VMESS = "vmess_id"


class AccessConfig:
    ip: str
    port: int
    is_active: bool
    # TODO: create a structure


class ProxyConfig(AccessConfig):
    def __init__(self, ip: str, port: int, login: str, password: str, is_active: bool = True):
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password
        self.is_active = is_active


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


class VpnConfig(AccessConfig):
    def __init__(self, uuid: str, ip: str, port: int, protocol: str, path: str, header_type: str = "", security: Security = Security(), remark: str = "", is_active: bool = True):
        self.uuid = uuid
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.path = path
        self.header_type = header_type
        self.security = security
        self.remark = remark
        self.is_active = is_active

    def create_string(self):
        return f"vless://{self.uuid}@{self.ip}:{self.port}?type={self.protocol}&path={self.path}&headerType={self.header_type}&security={self.security.create_string()}#{self.remark}"
