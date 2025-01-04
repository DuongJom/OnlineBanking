from enum import Enum

class TransactionType(Enum):
    TRANSFER = 0
    DEPOSIT = 1
    WITHDRAWAL = 2
    PAYMENT = 3
    INVESTMENT = 4