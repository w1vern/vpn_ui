from enum import Enum

class Role(Enum, str):
    admin = "admin"
    guest = "guest"
    member = "member"