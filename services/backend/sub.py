
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
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

from .depends import get_session

logger = setup_logger(__name__)


router = APIRouter(prefix="/sub")


@router.get(path="/{user_id}", include_in_schema=False)
async def get_subscriptions(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
) -> PlainTextResponse:
    logger.debug(user_id)
    result: list[str] = []
    ur = UserRepository(session)
    sr = ServerRepository(session)
    sir = ServerInboundRepository(session)
    apr = ActivePeriodRepository(session)
    user = await ur.get_by_id(user_id)
    if user is None:
        return PlainTextResponse(content="", status_code=404)
    ap = await apr.get_latest_for_user(user)
    if ap is None:
        return PlainTextResponse(content="", status_code=401)
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
    logger.debug(regrouped_inbds)
    logger.debug(servers)
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
                        string = inbd.template.format(user_id=user.id)
                    case _:
                        string = inbd.template
                result.append(f"{string}")
    return PlainTextResponse(content="\n\n".join(result), status_code=200)
