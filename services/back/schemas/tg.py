

from pydantic import BaseModel


class TgId(BaseModel):
    tg_id: int

class TgAuth(BaseModel):
    tg_id: int
    tg_code: str