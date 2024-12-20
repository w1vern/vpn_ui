

import enum


class Rights(enum.Enum):
    is_admin_rights_editor = 0b1 << 0
    is_member_rights_editor = 0b1 << 1
    is_users_editor = 0b1 << 2
    is_servers_editor = 0b1 << 3
    is_control_panel_user = 0b1 << 4
    is_verified = 0b1 << 5
    is_transactions_editor = 0b1 << 6
    is_active_periods_editor = 0b1 << 7
    is_tariffs_editor = 0b1 << 8
    can_use = 0b1 << 9