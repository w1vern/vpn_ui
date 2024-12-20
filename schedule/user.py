

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from _3x_ui_.service import Service
from _3x_ui_.session_manager import server_session_manager
from database.database import session_manager
from database.enums.rights import Rights
from database.enums.transaction_type import TransactionType
from database.models.user import User
from database.repositories.active_period_repository import \
    ActivePeriodRepository
from database.repositories.panel_server_repository import PanelServerRepository
from database.repositories.tariff_repository import TrafficRepository
from database.repositories.transaction_repository import TransactionRepository
from database.repositories.user_repository import UserRepository


async def check_users() -> None:
    async with session_manager.session() as db_session:
        ur = UserRepository(db_session)
        apr = ActivePeriodRepository(db_session)
        psr = PanelServerRepository(db_session)
        tr = TransactionRepository(db_session)
        users = await ur.get_all()
        servers = await psr.get_all()
        services: list[Service] = []
        for server in servers:
            async with server_session_manager.get_session(server) as server_session:
                services.append(Service(db_session, server_session))
        for user in users:
            if user.is_verified is False:
                continue

            last_active_periods = await apr.get_last_by_user_id(user)
            current_date = datetime.now(UTC).replace(tzinfo=None)
            traffic = 0
            for service in services:
                traffic += await service.get_traffic(user)

            if last_active_periods is None:
                if user.balance > user.tariff.price and user.auto_pay is True:
                    await tr.create(user, user.tariff.price, current_date, TransactionType.withdrawal.value)
                continue

            if last_active_periods.result_traffic != -1:
                if user.balance > user.tariff.price and user.auto_pay is True:
                    await ur.update_rights(user, {Rights.can_use.name: True})
                    await tr.create(user, user.tariff.price, current_date, TransactionType.withdrawal.value)
                    for service in services:
                        await service.set_enable(user, True, None)
                continue

            if last_active_periods.end_date <= current_date:
                await apr.close_period(last_active_periods, traffic, current_date)
                for service in services:
                    await service.reset_traffic(user)
                if user.auto_pay is True and user.balance > user.tariff.price:
                    await tr.create(user, user.tariff.price, current_date, TransactionType.withdrawal.value)
                else:
                    await ur.update_rights(user, {Rights.can_use.name: False})
                    for service in services:
                        await service.set_enable(user, False, None)
                continue

            if last_active_periods.end_date > current_date:
                if traffic > user.tariff.traffic:
                    await apr.close_period(last_active_periods, traffic, current_date)
                    for service in services:
                        await service.reset_traffic(user)
                    if user.auto_pay is True and user.balance > user.tariff.price_of_traffic_reset:
                        await tr.create(user, user.tariff.price, current_date, TransactionType.withdrawal.value)
                    else:
                        await ur.update_rights(user, {Rights.can_use.name: False})
                        for service in services:
                            await service.set_enable(user, False, None)
                continue
