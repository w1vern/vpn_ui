
from .base import (
    BaseCustomHTTPException,
)


class AccessTokenMissingException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Access token is missing")


class AccessTokenExpiredException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Access token has expired")


class AccessTokenInvalidatedException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Access token is invalidated")


class AccessTokenCorruptedException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Access token is corrupted")


class RefreshTokenMissingException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Refresh token is missing")


class RefreshTokenExpiredException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Refresh token has expired")


class RefreshTokenInvalidException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Invalid refresh token")


class LoginLockedException(BaseCustomHTTPException):
    def __init__(self, seconds: int) -> None:
        super().__init__(401, f"Login is locked for {seconds} seconds")


class TooManyAttemptsFromIPException(BaseCustomHTTPException):
    def __init__(self, ip: str) -> None:
        super().__init__(
            401, f"Too many incorrect login attempts from IP: {ip}")


class CodeNotFoundException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Telegram code not found")


class UserNotFoundException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "User not found")


class InvalidCredentialsException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Invalid credentials")


class UnauthorizedLogoutException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Unauthorized logout attempt")


class TooSoonToSendCodeException(BaseCustomHTTPException):
    def __init__(self, seconds: int) -> None:
        super().__init__(401, f"New code can be sent in {seconds} seconds")


class AuthIntegrityException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Authentication integrity check failed. Contact administrator.")


class RequestClientException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(401, "Request client not found")