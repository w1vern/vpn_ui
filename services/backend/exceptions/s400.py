
from .base import BaseBadRequestException


class PasswordsDoNotMatchException(BaseBadRequestException):
    def __init__(self) -> None:
        super().__init__("Passwords do not match")


class ServerAlreadyExistsException(BaseBadRequestException):
    def __init__(self) -> None:
        super().__init__("Server already exists")


class ServerCreationFailedException(BaseBadRequestException):
    def __init__(self) -> None:
        super().__init__("Server creation failed")


class InvalidTicketDataException(BaseBadRequestException):
    def __init__(self) -> None:
        super().__init__("Invalid ticket data")
