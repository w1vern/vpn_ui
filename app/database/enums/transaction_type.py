from enum import Enum

class TransactionType(Enum, str):
    refund = "refund"
    replenishment = "replenishment"
    withdrawal = "withdrawal"