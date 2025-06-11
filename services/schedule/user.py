

from datetime import UTC, datetime

from shared._3x_ui_ import Service, server_session_manager
from shared.database import (ActivePeriodRepository, PanelServerRepository,
                             Rights, TransactionRepository, TransactionType,
                             UserRepository, session_manager)


async def check_users() -> None:
    async with session_manager.context_session() as db_session:
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
                        trans = await tr.create(user, user.tariff.price, current_date, TransactionType.withdrawal.value)
                        if not trans:
                            raise Exception("Transaction is None")
                        await apr.close_period(last_active_periods, traffic, current_date)
                        await apr.create(user, trans, user.tariff, current_date, last_active_periods.end_date)
                    else:
                        await ur.update_rights(user, {Rights.can_use.name: False})
                        for service in services:
                            await service.set_enable(user, False, None)
                continue
