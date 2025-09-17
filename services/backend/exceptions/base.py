
from fastapi import (
    HTTPException,
)


class BaseCustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)
