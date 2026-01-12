
from uuid import UUID

from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .api import router
from .depends import get_session
from .rabbit import router as faststream_router
from .response import SuccessResponse
from .sub import get_subscriptions

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    swagger_ui_parameters={
        "tryItOutEnabled": True
    })


@router.get("/health", include_in_schema=False)
async def health() -> SuccessResponse:
    return SuccessResponse()


@app.get("/sub/{user_id}", include_in_schema=False)
async def subscriptions(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
) -> PlainTextResponse:
    ans, status = await get_subscriptions(user_id, session)
    return PlainTextResponse(content=ans, status_code=status)

app.include_router(router)
app.include_router(faststream_router)
