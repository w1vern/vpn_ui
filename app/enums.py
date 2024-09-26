from enum import Enum

class TransactionType(Enum, str):
    refund = "refund"
    replenishment = "replenishment"
    withdrawal = "withdrawal"

class Role(Enum, str):
    admin = "admin"
    guest = "guest"
    member = "member"

