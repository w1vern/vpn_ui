
from back.api import router
from back.broker import router as faststream_router
from fastapi import FastAPI

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json")
app.include_router(router)
app.include_router(faststream_router)