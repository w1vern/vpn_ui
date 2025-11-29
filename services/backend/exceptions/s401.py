
from .base import BaseUnauthorizedException


class AccessTokenMissingException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Access token is missing")


class AccessTokenExpiredException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Access token has expired")


class AccessTokenInvalidatedException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Access token is invalidated")


class AccessTokenCorruptedException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Access token is corrupted")


class RefreshTokenMissingException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Refresh token is missing")


class RefreshTokenExpiredException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Refresh token has expired")


class RefreshTokenInvalidException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Invalid refresh token")


class LoginLockedException(BaseUnauthorizedException):
    def __init__(self, seconds: int) -> None:
        super().__init__(f"Login is locked for {seconds} seconds")


class TooManyAttemptsFromIPException(BaseUnauthorizedException):
    def __init__(self, ip: str) -> None:
        super().__init__(f"Too many incorrect login attempts from IP: {ip}")


class CodeNotFoundException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Telegram code not found")


class UserNotFoundException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("User not found")


class InvalidCredentialsException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Invalid credentials")


class UnauthorizedLogoutException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Unauthorized logout attempt")


class TooSoonToSendCodeException(BaseUnauthorizedException):
    def __init__(self, seconds: int) -> None:
        super().__init__(f"New code can be sent in {seconds} seconds")


class AuthIntegrityException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Authentication integrity check failed. Contact administrator.")


class RequestClientException(BaseUnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Request client not found")
