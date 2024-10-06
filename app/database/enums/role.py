from enum import Enum

class Role(str, Enum):
    admin = "admin"
    guest = "guest"
    member = "member"