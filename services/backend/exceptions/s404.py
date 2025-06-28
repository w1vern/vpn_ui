
from .base import BaseCustomHTTPException


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


class UserNotFoundException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(404, "User not found")

class TransactionNotFoundException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(404, "Transaction not found")

class TariffNotFoundException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(404, "Tariff not found")
