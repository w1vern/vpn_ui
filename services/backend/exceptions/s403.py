
from .base import BaseCustomHTTPException


class NotControlPanelUserException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(403, "User is not a control panel member")


class NotServerEditorException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(403, "User is not a server editor")


class NoPermissionException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(403, "User does not have permission")


class AdminRightsEditNotAllowedException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(403, "You cannot edit admin rights")


class MemberRightsEditNotAllowedException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(403, "You cannot edit member rights")


class UserNotTransactionEditorException(BaseCustomHTTPException):
    def __init__(self) -> None:
        super().__init__(403, "User is not a transaction editor")
