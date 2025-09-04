
from .base import BaseCustomHTTPException

class InvalidDateFormatException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(422, "Invalid date format")