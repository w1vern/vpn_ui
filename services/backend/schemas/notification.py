
from pydantic import BaseModel
from shared.database import LanguageCodes

class Notification(BaseModel):
    data: dict[LanguageCodes, str]

    