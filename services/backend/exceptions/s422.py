
from .base import BaseUnprocessableEntityException


class InvalidDateFormatException(BaseUnprocessableEntityException):
    def __init__(self) -> None:
        super().__init__("Invalid date format")