
from .base import BaseConflictException


class TariffAlreadyExistsException(BaseConflictException):
    def __init__(self) -> None:
        super().__init__(detail="Tariff already exists")
