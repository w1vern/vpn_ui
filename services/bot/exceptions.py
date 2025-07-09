
import inspect
import traceback


class BaseCustomException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class MessageUserIsNoneException(BaseCustomException):
    def __init__(self):
        super().__init__("Message from_user is None")


class UserNotFoundException(BaseCustomException):
    def __init__(self):
        super().__init__("User not found")


class MessageUsernameIsNoneException(BaseCustomException):
    def __init__(self):
        super().__init__("Message from_user.username is None")


class IncorrectStateException(BaseCustomException):
    def __init__(self, state: str):
        super().__init__(f"Incorrect state: {state}")

class MessageTextIsNoneException(BaseCustomException):
    def __init__(self):
        super().__init__("Message.text is None")

class SendFeedbackToAdminException(BaseCustomException):
    def __init__(self):
        current_frame = inspect.currentframe()
        message = ""
        if current_frame:
            outer_frame = current_frame.f_back
            if outer_frame:
                filename = outer_frame.f_code.co_filename
                lineno = outer_frame.f_lineno
                function = outer_frame.f_code.co_name
                message += f"File: {filename}\nLine: {lineno}\nFunction: {function}\n"
        stack_trace = "".join(traceback.format_stack())
        message += f"Stack Trace:\n{stack_trace}"

        super().__init__("".join([
            "Interesting error occurred.",
            "Please contact the administrator for assistance.",
            "\n\nAdditional information:\n",
            message]))
