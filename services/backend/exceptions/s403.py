
from .base import BaseForbiddenException


class NotControlPanelUserException(BaseForbiddenException):
    def __init__(self) -> None:
        super().__init__("User is not a control panel member")


class NotServerEditorException(BaseForbiddenException):
    def __init__(self) -> None:
        super().__init__("User is not a server editor")


class AdminRightsEditNotAllowedException(BaseForbiddenException):
    def __init__(self) -> None:
        super().__init__("You cannot edit admin rights")


class MemberRightsEditNotAllowedException(BaseForbiddenException):
    def __init__(self) -> None:
        super().__init__("You cannot edit member rights")


class MemberSettingsEditNotAllowedException(BaseForbiddenException):
    def __init__(self) -> None:
        super().__init__("You cannot edit member settings")


class UserNotTransactionEditorException(BaseForbiddenException):
    def __init__(self) -> None:
        super().__init__("User is not a transaction editor")


class NotTariffEditorException(BaseForbiddenException):
    def __init__(self) -> None:
        super().__init__("User is not a tariff editor")
