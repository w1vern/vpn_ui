

import enum


class Settings(enum.Enum):
    get_traffic_notifications = 0b1 << 0
    auto_pay = 0b1 << 1
    is_active = 0b1 << 2