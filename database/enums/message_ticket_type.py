from enum import Enum


class MessageTicketType(Enum):
    from_admin = 0b1 << 0
    from_user = 0b1 << 1