
from .exceptions import IncorrectStateException


class MyState():
    def __init__(self,
                 state: str,
                 parent_state: "MyState | None" = None
                 ) -> None:
        self._state = state
        self._parent = parent_state

    @property
    def to_str(self) -> str:
        if not self._parent is None:
            return f"{self._parent.to_str}/{self._state}"
        return self._state

    @classmethod
    def from_str(cls, state: str) -> 'MyState':
        last_state = state.split("/")[-1]
        for key, value in user_attrs.items():
            if value.to_str == last_state:
                return AppStates.__dict__[key]
        raise IncorrectStateException(state)


class AppStates():
    main_menu = MyState("main_menu")
    ticket = MyState("ticket", main_menu)
    inbounds_menu = MyState("connections_menu", main_menu)
    settings_menu = MyState("settings_menu", main_menu)
    info_menu = MyState("info_menu", main_menu)


user_attrs = {
    key: value
    for key, value in AppStates.__dict__.items()
    if not key.startswith('__') and not callable(value)
}
