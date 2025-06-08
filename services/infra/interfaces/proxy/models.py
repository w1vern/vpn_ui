

import abc
import json
from enum import Enum
from typing import Any
from uuid import UUID


class AccessType(str, Enum):
    HTTP = "http_id"
    SOCKS = "socks_id"
    VLESS = "vless_id"
    VLESS_REALITY = "vless_reality_id"
    VMESS = "vmess_id"


class ProxyType(str, Enum):
    HTTP = AccessType.HTTP.value
    SOCKS = AccessType.SOCKS.value


class VpnType(str, Enum):
    VLESS = AccessType.VLESS.value
    VLESS_REALITY = AccessType.VLESS_REALITY.value
    VMESS = AccessType.VMESS.value


class AccessConfig(abc.ABC):
    id: int
    class_name: str
    ip: str
    port: int
    access_type: AccessType

    @abc.abstractmethod
    def create_string(self) -> str: ...

    @abc.abstractmethod
    def to_string(self) -> str: ...

    @classmethod
    def from_string(cls, access_config_str: str) -> 'AccessConfig': ...


class AccessConfigFactory:
    __registry: dict[str, AccessConfig] = {}

    @classmethod
    def register(cls, name, config_class):
        cls.__registry[name] = config_class

    @classmethod
    def from_string(cls, access_config_str):
        d = json.loads(access_config_str)
        name = d['class_name']
        if name not in cls.__registry:
            raise ValueError(f"No registered class for name: {name}")
        return cls.__registry[name].from_string(access_config_str)

    @classmethod
    def register_with_decorator(cls):
        def decorator(config_class):
            cls.register(config_class.__name__, config_class)
            return config_class
        return decorator


@AccessConfigFactory.register_with_decorator()
class ProxyConfig(AccessConfig):
    def __init__(self,
                 id: int,
                 access_type: AccessType,
                 ip: str,
                 port: int,
                 login: str,
                 password: str,
                 is_active: bool = True):
        self.id = id
        self.access_type = access_type
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password
        self.is_active = is_active
        self.class_name = self.__class__.__name__

    def create_string(self) -> str:
        return f"http://{self.login}:{self.password}@{self.ip}:{self.port}"

    def to_string(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_string(cls, access_config_str: str) -> 'AccessConfig':
        proxy_dict = json.loads(access_config_str)
        del (proxy_dict['class_name'])
        return ProxyConfig(**proxy_dict)


class Security(abc.ABC):

    @abc.abstractmethod
    def create_string(self) -> str: ...

    @abc.abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    def from_dict(cls, security_dict: dict[str, Any]) -> 'Security': ...


class SecurityFactory:
    __registry: dict[str, Security] = {}

    @classmethod
    def register(cls, name, security_class):
        cls.__registry[name] = security_class

    @classmethod
    def from_dict(cls, security_dict: dict[str, Any]):
        name = security_dict['class_name']
        if name not in cls.__registry:
            raise ValueError(f"No registered class for name: {name}")
        return cls.__registry[name].from_dict(security_dict)

    @classmethod
    def register_with_decorator(cls):
        def decorator(security_class):
            cls.register(security_class.__name__, security_class)
            return security_class
        return decorator


@SecurityFactory.register_with_decorator()
class NoneSecurity(Security):

    def __init__(self) -> None:
        self.class_name = self.__class__.__name__

    def create_string(self) -> str:
        return 'none'

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, security_dict: dict[str, Any]) -> Security:
        del (security_dict['class_name'])
        return cls(**security_dict)


@SecurityFactory.register_with_decorator()
class RealityOptions(Security):
    def __init__(self, public_key: str, fp: str, server_name_indication: str, sid: str, spx: str):
        self.security_name = "reality"
        self.public_key = public_key
        self.fp = fp
        self.server_name_indication = server_name_indication
        self.sid = sid
        self.spx = spx
        self.class_name = self.__class__.__name__

    def create_string(self) -> str:
        return f"{self.security_name}&pbk={self.public_key}&fp={self.fp}&sni={self.server_name_indication}&sid={self.sid}&spx={self.spx}"

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, security_dict: dict[str, Any]) -> Security:
        del (security_dict['class_name'])
        del (security_dict['security_name'])
        return cls(**security_dict)


@AccessConfigFactory.register_with_decorator()
class VpnConfig(AccessConfig):
    def __init__(self,
                 id: int,
                 access_type: AccessType,
                 uuid: UUID,
                 ip: str,
                 port: int,
                 protocol: str,
                 path: str,
                 header_type: str = "",
                 security: Security = NoneSecurity(),
                 remark: str = "",
                 is_active: bool = True
                 ) -> None:
        self.id = id
        self.access_type = access_type
        self.uuid = uuid
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.path = path
        self.header_type = header_type
        self.security = security
        self.remark = remark
        self.is_active = is_active
        self.class_name = self.__class__.__name__

    def create_string(self):
        return "".join([
            f"vless://{self.uuid}@{self.ip}:{self.port}",
            f"?type={self.protocol}&path={self.path}",
            f"&headerType={self.header_type}",
            f"&security={self.security.create_string()}#{self.remark}"])

    def to_string(self) -> str:
        ans = self.__dict__
        ans['security'] = ans['security'].to_dict()
        return json.dumps(self.__dict__)

    @classmethod
    def from_string(cls, access_config_str: str) -> 'AccessConfig':
        vpn_dict = json.loads(access_config_str)
        security_dict = vpn_dict['security']
        security = SecurityFactory.from_dict(security_dict)
        vpn_dict['security'] = security
        del (vpn_dict['class_name'])
        return cls(**vpn_dict)
