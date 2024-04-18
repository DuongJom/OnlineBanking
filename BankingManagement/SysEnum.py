from enum import Enum

class SexType(Enum):
    MALE = 0
    FEMALE = 1
    OTHER = 2

class RoleType(Enum):
    USER = 0
    EMPLOYEE = 1
    ADMIN = 2

class CardType(Enum):
    CREDITS=0
    DEBITS = 1