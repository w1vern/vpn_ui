
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    ActivePeriodRepository,
    ServerInbound,
    ServerInboundRepository,
    ServerRepository,
    UserRepository
)
from shared.infrastructure import setup_logger
from shared.x_ui import PanelRepository, server_session_manager

logger = setup_logger(__name__)


async def get_subscriptions(
    user_id: UUID,
    session: AsyncSession
) -> tuple[str, int]:
    result: list[str] = []
    ur = UserRepository(session)
    sr = ServerRepository(session)
    sir = ServerInboundRepository(session)
    apr = ActivePeriodRepository(session)
    user = await ur.get_by_id(user_id)
    if user is None:
        return "", 404
    ap = await apr.get_latest_for_user(user)
    if ap is None:
        return "", 401
    use_unawailable = ap.tariff.with_unavalable_inbounds
    servers = await sr.get_all()

    def regroup_inbounds(
        inbds: list[ServerInbound]
    ) -> dict[UUID, list[ServerInbound]]:
        res = {}
        for inbd in inbds:
            if inbd.server_id not in res:
                res[inbd.server_id] = []
            res[inbd.server_id].append(inbd)
        return res
    inbds = await sir.get_all()
    regrouped_inbds = regroup_inbounds(inbds)
    for server in servers:
        server_inbds = regrouped_inbds[server.id]
        async with server_session_manager.get_session(server) as server_session:
            pr = PanelRepository(server_session)
            for inbd in server_inbds:
                if not (use_unawailable or inbd.is_available):
                    continue
                await pr.ensure_user_exists(user=user, server_inbound=inbd)
                match inbd.protocol:
                    case "vless":
                        string = inbd.template.format(
                            user_id=user.id,
                            comment=f"{inbd.name}-{inbd.description}")
                    case _:
                        string = inbd.template
                result.append(f"{string}")
    return "\n\n".join(result), 200
