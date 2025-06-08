from enum import Enum

from .rights import Rights


class RightsType(Enum):
    super_admin = (0b1 << 15) - 1
    admin = Rights.is_member_rights_editor.value + \
        Rights.is_servers_editor.value + \
        Rights.is_control_panel_user.value + \
        Rights.is_verified.value + \
        Rights.can_use.value
    member = Rights.is_verified.value + \
        Rights.can_use.value
    guest = 0
