

from email.policy import default
import enum


class SettingsType(enum.Enum):
    default = 0b1 << 15 - 1