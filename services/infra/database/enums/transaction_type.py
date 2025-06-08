
from enum import Enum


class TransactionType(str, Enum):
    refund = "refund"
    replenishment = "replenishment"
    withdrawal = "withdrawal"