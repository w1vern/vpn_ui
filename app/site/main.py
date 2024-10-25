
from fastapi import FastAPI, Depends, HTTPException

from app.site.api import router
from app.site.broker import router as faststream_router

app = FastAPI()
app.include_router(router)
app.include_router(faststream_router)