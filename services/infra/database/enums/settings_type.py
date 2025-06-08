

import enum
from email.policy import default


class SettingsType(enum.Enum):
    default = (0b1 << 15) - 1