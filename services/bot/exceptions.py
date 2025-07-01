
class BaseException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class MessageUserIsNoneException(BaseException):
    def __init__(self):
        super().__init__("Message from_user is None")


class UserNotFoundException(BaseException):
    def __init__(self):
        super().__init__("User not found")


class MessageUsernameIsNoneException(BaseException):
    def __init__(self):
        super().__init__("Message from_user.username is None")


class IncorrectStateException(BaseException):
    def __init__(self, state: str):
        super().__init__(f"Incorrect state: {state}")
