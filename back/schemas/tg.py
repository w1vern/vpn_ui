

from pydantic import BaseModel


class TgId(BaseModel):
    tg_id: str

class TgAuth(BaseModel):
    tg_id: str
    tg_code: str