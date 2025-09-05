
import inspect
import traceback

from .i18n import I18nMessage, MessageKey


class BaseCustomException(Exception):
    def __init__(self, detail: I18nMessage):
        self.detail = detail


class MessageUserIsNoneException(BaseCustomException):
    def __init__(self):
        super().__init__(I18nMessage(MessageKey.message_user_is_none_exception))


class UserNotFoundException(BaseCustomException):
    def __init__(self):
        super().__init__(I18nMessage(MessageKey.user_not_found_exception))


class MessageUsernameIsNoneException(BaseCustomException):
    def __init__(self):
        super().__init__(I18nMessage(MessageKey.message_username_is_none_exception))


class IncorrectStateException(BaseCustomException):
    def __init__(self, state: str):
        super().__init__(I18nMessage(MessageKey.incorrect_state_exception, state=state))


class MessageTextIsNoneException(BaseCustomException):
    def __init__(self):
        super().__init__(I18nMessage(MessageKey.message_text_is_none_exception))


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

        super().__init__(I18nMessage(
            MessageKey.send_feedback_to_admin_exception,
            additional_info=message))
