
from .base import BaseNotFoundException


class ServerNotFoundException(BaseNotFoundException):
    def __init__(self) -> None:
        super().__init__("Server not found")
        
class ServerInboundNotFoundException(BaseNotFoundException):
    def __init__(self) -> None:
        super().__init__("Server inbound not found")


class TargetUserNotFoundException(BaseNotFoundException):
    def __init__(self) -> None:
        super().__init__("Target user does not exist")


class TransactionTypeNotFoundException(BaseNotFoundException):
    def __init__(self) -> None:
        super().__init__("Transaction type does not exist")


class TicketNotFoundException(BaseNotFoundException):
    def __init__(self) -> None:
        super().__init__("Ticket not found")


class UserNotFoundException(BaseNotFoundException):
    def __init__(self) -> None:
        super().__init__("User not found")


class TransactionNotFoundException(BaseNotFoundException):
    def __init__(self) -> None:
        super().__init__("Transaction not found")


class TariffNotFoundException(BaseNotFoundException):
    def __init__(self) -> None:
        super().__init__("Tariff not found")
