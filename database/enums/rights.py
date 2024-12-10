

import enum
from os import close

from click import edit


class Rights(enum.Enum):
    edit_admin_rights = 0b1 << 0
    edit_member_rights = 0b1 << 1
    edit_users = 0b1 << 2
    edit_servers = 0b1 << 3
    use_control_panel = 0b1 << 4
    verified = 0b1 << 5
    edit_transactions = 0b1 << 6
    edit_active_periods = 0b1 << 7
    edit_tariffs = 0b1 << 8
    active = 0b1 << 9