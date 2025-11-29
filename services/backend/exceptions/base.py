
from fastapi import HTTPException


class BaseCustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)


class BaseBadRequestException(BaseCustomHTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=400, detail=detail)


class BaseUnauthorizedException(BaseCustomHTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=401, detail=detail)


class BaseForbiddenException(BaseCustomHTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=403, detail=detail)


class BaseNotFoundException(BaseCustomHTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=404, detail=detail)


class BaseConflictException(BaseCustomHTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=409, detail=detail)


class BaseUnprocessableEntityException(BaseCustomHTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=422, detail=detail)


class BaseInternalServerErrorException(BaseCustomHTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=500, detail=detail)
