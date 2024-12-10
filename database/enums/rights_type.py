from enum import Enum

from database.enums.rights import Rights


class RightsType(Enum):
    super_admin = 0b1 << 15 - 1
    admin = Rights.edit_member_rights.value + \
        Rights.edit_servers.value + \
        Rights.use_control_panel.value + \
        Rights.verified.value + \
        Rights.active.value
    member = Rights.verified.value + \
        Rights.active.value
    guest = 0
