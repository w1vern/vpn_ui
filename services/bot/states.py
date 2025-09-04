
from shared.infrastructure import setup_logger

from .exceptions import IncorrectStateException

logger = setup_logger(__name__)


class MyState():
    def __init__(self,
                 state: str,
                 parent_state: "MyState | None" = None
                 ) -> None:
        self._state = state
        self._parent = parent_state

    def __str__(self) -> str:
        return self.string

    @property
    def string(self) -> str:
        if not self._parent is None:
            return f"{self._parent.string}/{self._state}"
        return self._state

    @classmethod
    def from_str(cls, state: str) -> 'MyState':
        for key, value in user_attrs.items():
            if value.string == state:
                return AppStates.__dict__[key]
        raise IncorrectStateException(state)


class AppStates():
    main_menu = MyState("main_menu")
    ticket_menu = MyState("ticket_menu", main_menu)
    inbounds_menu = MyState("inbounds_menu", main_menu)
    settings_menu = MyState("settings_menu", main_menu)
    info_menu = MyState("info_menu", main_menu)
    transactions_menu = MyState("transactions_menu", main_menu)


user_attrs = {
    key: value
    for key, value in AppStates.__dict__.items()
    if not key.startswith('__') and not callable(value)
}
