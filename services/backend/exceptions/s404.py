
from .base import (
    BaseCustomHTTPException,
)


class ServerNotFoundException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(404, "Server not found")


class TargetUserNotFoundException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(404, "Target user does not exist")


class TransactionTypeNotFoundException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(404, "Transaction type does not exist")


class TicketNotFoundException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(404, "Ticket not found")
