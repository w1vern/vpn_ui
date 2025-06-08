

import random
import secrets
import string
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from _3x_ui_.repository import PanelRepository
from _3x_ui_.session_manager import ServerSession
from infra.database.models import PanelServer, User
from infra.database.repositories import (PanelServerRepository,
                                   ServerUserInboundRepository)
from interfaces.proxy.interface import ProxyInterface
from interfaces.proxy.models import (AccessConfig, AccessType, NoneSecurity,
                                     ProxyConfig, ProxyType, RealityOptions,
                                     VpnConfig, VpnType)


def generate_sub_id(length: int = 16) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_short_ids(count: int = 1) -> list[str]:
    res = []
    for i in range(count):
        length = random.randint(16, 16)
        res.append(
            hex(random.randint(0b1 << 4 * (length-1), 0b1 << 4 * length))[2:])
    return res


def generate_email(user: User, vpn_type: VpnType) -> str:
    return f"{user.telegram_username}-{vpn_type.value[:-3]}-{uuid.uuid4()}"


def generate_vpn_remark(vpn_type: VpnType) -> str:
    return f"{vpn_type.value[:-3]}"


def generate_proxy_remark(server: PanelServer, user: User, proxy_type: ProxyType) -> str:
    return f"{proxy_type.value[:-3]}-{user.telegram_username}"


def generate_user_remark(server: PanelServer, user: User, vpn_type: VpnType) -> str:
    return f"{server.country_code}-{server.display_name}-{user.telegram_username}-{vpn_type.value[:-3]}"


def generate_key(length: int = 43) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits + "-_", k=length))


class Service(ProxyInterface):
    def __init__(self, db_session: AsyncSession, server_session: ServerSession) -> None:
        self.__db_session = db_session
        self.__server_session = server_session
        self.__pr = PanelRepository(server_session)
        self.__psr = PanelServerRepository(db_session)
        self.__suir = ServerUserInboundRepository(db_session)

    async def get_config(self,
                         user: User,
                         access_type: AccessType = AccessType.HTTP,
                         create_if_not_exists: bool = True,
                         login: str = "",
                         password: str = ""
                         ) -> AccessConfig | None:
        inbounds = await self.__suir.get_by_server_and_user(self.__server_session.server, user)
        for inbound in inbounds:
            if inbound.access_type == access_type:
                if await self.config_is_valid(user, inbound.config) is True:
                    return inbound.config
                break
        if create_if_not_exists is False:
            return None
        if access_type in ProxyType:
            response = await self.__create_proxy(user, login, password, ProxyType(access_type))
        elif access_type in VpnType:
            response = await self.__create_vpn_user(user, VpnType(access_type))
        else:
            return None
        if response is None:
            return None
        await self.__suir.create(self.__server_session.server, user, response)
        return response

    # TODO: create valid code
    async def config_is_valid(self, user: User, config: AccessConfig) -> bool:
        return True

    async def __create_proxy(self,
                             user: User,
                             login: str = "",
                             password: str = "",
                             proxy_type: ProxyType = ProxyType.HTTP,
                             ) -> ProxyConfig | None:
        if login == "":
            login = secrets.token_urlsafe(8)
        if password == "":
            password = secrets.token_urlsafe(8)
        response = await self.__pr.create_proxy(
            remark=generate_proxy_remark(
                self.__server_session.server, user, proxy_type),
            login=login,
            password=password,
            port=await self.__pr.get_free_port(),
            proxy_type=proxy_type)
        if response['success'] is False:
            return None
        return ProxyConfig(id=response['obj']['id'],
                           access_type=AccessType(proxy_type.value),
                           ip=self.__server_session.server.ip,
                           port=response['obj']['port'],
                           login=response['obj']['settings']['accounts'][0]['user'],
                           password=response['obj']['settings']['accounts'][0]['pass'])

    async def __create_vpn_user(self,
                                user: User,
                                vpn_type: VpnType = VpnType.VLESS_REALITY,
                                ) -> VpnConfig | None:
        uuid4 = uuid.uuid4()
        sub_id = generate_sub_id()
        email = generate_email(user, vpn_type)
        protocol = vpn_type.value[:-3]
        if vpn_type == VpnType.VLESS_REALITY:
            protocol = "vless"
        if getattr(self.__server_session.server, vpn_type.value) == 0:
            remark = generate_vpn_remark(vpn_type)
            short_ids = generate_short_ids()
            port = await self.__pr.get_free_port()
            public_key = generate_key()
            private_key = generate_key()
            response = await self.__pr.create_vpn(remark=remark,
                                                  protocol=protocol,
                                                  user=user, sub_id=sub_id,
                                                  short_ids=short_ids,
                                                  vpn_type=vpn_type,
                                                  uuid4=uuid4,
                                                  port=port,
                                                  email=email,
                                                  public_key=public_key,
                                                  private_key=private_key)
            if response['success'] is False:
                return None
            await self.__psr.update_vpn(server=self.__server_session.server,
                                        id=response['obj']['id'],
                                        port=port,
                                        domain_short_id=short_ids[0],
                                        vpn_type=vpn_type,
                                        public_key=public_key,
                                        private_key=private_key)
        else:
            response = await self.__pr.create_vpn_user(user=user,
                                                       vpn_type=vpn_type,
                                                       uuid4=uuid4,
                                                       sub_id=sub_id,
                                                       email=email)
            if response['success'] is False:
                return None
        security = NoneSecurity()
        if vpn_type == VpnType.VLESS_REALITY:
            security = RealityOptions(public_key=self.__server_session.server.vless_reality_public_key,
                                      fp="random",
                                      server_name_indication="yahoo.com",
                                      sid=getattr(self.__server_session.server,
                                                  f"{vpn_type.value[:-3]}_domain_short_id"),
                                      spx="/", )
        return VpnConfig(id=response['obj']['id'],
                         access_type=AccessType(vpn_type.value),
                         uuid=uuid4,
                         ip=self.__server_session.server.ip,
                         port=getattr(self.__server_session.server,
                         f"{vpn_type.value[:-3]}_port"),
                         protocol=protocol,
                         path="",
                         header_type="http",
                         security=security,
                         remark=generate_user_remark(self.__server_session.server, user, vpn_type))

    async def set_enable(self,
                         user: User,
                         enable: bool,
                         access_type: AccessType | None = None,
                         ) -> None:
        if access_type is None:
            for proxy_type in ProxyType:
                await self.__set_proxy_enable(user, proxy_type, enable)
            for vpn_type in VpnType:
                await self.__set_vpn_user_enable(user, vpn_type, enable)
            return
        elif access_type in ProxyType:
            return await self.__set_proxy_enable(user, ProxyType(access_type), enable)
        elif access_type in VpnType:
            return await self.__set_vpn_user_enable(user, VpnType(access_type), enable)
        else:
            return

    async def __set_proxy_enable(self,
                                 user: User,
                                 proxy_type: ProxyType,
                                 enable: bool
                                 ) -> None:
        connection = await self.__suir.get_by_server_user_access_type(self.__server_session.server, user, AccessType(proxy_type))
        if connection is None:
            raise Exception()
        response = await self.__pr.set_inbound_enabled(connection.config.id, enable)
        if response['success'] is False:
            raise Exception()
        return

    async def __set_vpn_user_enable(self, user: User, vpn_type: VpnType, enable: bool) -> None:

        connection = await self.__suir.get_by_server_user_access_type(self.__server_session.server,
                                                                      user,
                                                                      AccessType(vpn_type))
        if connection is None:
            raise Exception()
        assert isinstance(connection.config, VpnConfig)
        response = await self.__pr.set_vpn_user_enabled(getattr(self.__server_session.server,
                                                                vpn_type.value),
                                                        connection.config.uuid,
                                                        enable)
        if response['success'] is False:
            raise Exception()
        return

    async def delete(self, user: User, access_type: AccessType | None) -> None:
        if access_type is None:
            for proxy_type in ProxyType:
                await self.__delete_proxy(user, proxy_type)
            for vpn_type in VpnType:
                await self.__delete_vpn_user(user, vpn_type)
            return
        elif access_type in ProxyType:
            return await self.__delete_proxy(user, ProxyType(access_type))
        elif access_type in VpnType:
            return await self.__delete_vpn_user(user, VpnType(access_type))
        else:
            return

    async def __delete_proxy(self, user: User, proxy_type: ProxyType) -> None:
        connection = await self.__suir.get_by_server_user_access_type(self.__server_session.server, user, AccessType(proxy_type))
        if connection is None:
            raise Exception()
        response = await self.__pr.delete_inbound(connection.config.id)
        if response['success'] is False:
            raise Exception()
        return

    async def __delete_vpn_user(self, user: User, vpn_type: VpnType) -> None:
        connection = await self.__suir.get_by_server_user_access_type(self.__server_session.server, user, AccessType(vpn_type))
        if connection is None:
            raise Exception()
        response = await self.__pr.delete_vpn_user(connection.config.id,
                                                   connection.config.uuid)  # type: ignore
        if response['success'] is False:
            raise Exception()
        return

    async def get_configs(self, user: User) -> list[AccessConfig]:
        connections = await self.__suir.get_by_server_and_user(self.__server_session.server, user)
        configs = []
        for connection in connections:
            if not self.config_is_valid(user, connection.config):
                del (connections[connections.index(connection)])
            else:
                configs.append(connection.config)
        return configs

    async def get_traffic(self, user: User) -> int:
        connections = await self.__suir.get_by_server_and_user(self.__server_session.server, user)
        traffic = 0
        for connection in connections:
            if connection.access_type in ProxyType:
                response = await self.__pr.get_inbound_info(connection.config.id)
                traffic += response['obj']['up']
                traffic += response['obj']['down']
            elif connection.access_type in VpnType:
                response = await self.__pr.get_vpn_user_traffic(connection.config.id,
                                                                connection.config.uuid)  # type: ignore

                traffic += response['obj']['up']
                traffic += response['obj']['down']
        return traffic

    async def reset_traffic(self, user: User) -> None:
        connections = await self.__suir.get_by_server_and_user(self.__server_session.server, user)
        for connection in connections:
            if connection.access_type in ProxyType:
                await self.__pr.reset_proxy_traffic(connection.config.id)
            elif connection.access_type in VpnType:
                await self.__pr.reset_vpn_user_traffic(generate_email(user, VpnType(connection.access_type)))
