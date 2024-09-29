from enum import Enum

class MessageTicketType(Enum, str):
    from_admin = "from_admin"
    from_user = "from_user"
    to_all = "to_all"