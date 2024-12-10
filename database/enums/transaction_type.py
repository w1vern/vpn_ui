from enum import Enum


class TransactionType(Enum):
    refund = 0b1 << 0
    replenishment = 0b1 << 1
    withdrawal = 0b1 << 2