
from aiogram.fsm.state import State, StatesGroup


class MyState(State):
    def __init__(self,
                 state: str,
                 parent_state: "MyState | None" = None
                 ) -> None:
        self._state = state
        self._group_name = None
        self._group: type[StatesGroup] | None = None
        self._parent = parent_state

    @property
    def state(self) -> str:
        if self._parent:
            return f"{self._parent.state}/{self._state}"
        return self._state


class AppState(StatesGroup):
    main_menu = MyState("main_menu")
    ticket = MyState("ticket", main_menu)
    inbounds_menu = MyState("connections_menu", main_menu)
    settings_menu = MyState("settings_menu", main_menu)
    info_menu = MyState("info_menu", main_menu)
