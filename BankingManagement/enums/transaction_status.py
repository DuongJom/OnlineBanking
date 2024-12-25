from enum import Enum

class TransactionStatus(Enum):
    SUCCESS = 0
    FAILED = 1
    PENDING = 2
    DOING = 3