
from fastapi import Depends, FastAPI, HTTPException

from back.api import router
from back.broker import router as faststream_router

app = FastAPI()
app.include_router(router)
app.include_router(faststream_router)