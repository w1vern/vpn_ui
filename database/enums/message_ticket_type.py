
from enum import Enum


class MessageTicketType(str, Enum):
    from_admin = "from_admin"
    from_user = "from_user"
