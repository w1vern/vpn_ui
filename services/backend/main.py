
from fastapi import FastAPI

from .api import router
from .rabbit import router as faststream_router

app = FastAPI(docs_url="/api/docs",
              redoc_url="/api/redoc",
              openapi_url="/api/openapi.json",
              swagger_ui_parameters={
                  "tryItOutEnabled": True,
              })
app.include_router(router)
app.include_router(faststream_router)
