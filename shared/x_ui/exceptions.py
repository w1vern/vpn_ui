
class BaseXUIException(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail


class UnauthorizedException(BaseXUIException):
    def __init__(self) -> None:
        super().__init__("x-ui authorization failed")


class UnexpectedFailureException(BaseXUIException):
    def __init__(self) -> None:
        super().__init__("x-ui unexpected failure")
        
class UndefinedException(BaseXUIException):
    def __init__(self, detail: str) -> None:
        super().__init__(f"x-ui undefined failure. Detail: {detail}")
