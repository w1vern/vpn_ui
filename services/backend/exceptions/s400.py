
from .base import (
    BaseCustomHTTPException,
)


class PasswordsDoNotMatchException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Passwords do not match")


class ServerAlreadyExistsException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Server already exists")


class ServerCreationFailedException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Server creation failed")


class InvalidTicketDataException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(400, "Invalid ticket data")
