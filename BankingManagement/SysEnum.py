from enum import Enum

class SexEnum(Enum):
    MALE = 0
    FEMALE = 1
    OTHER = 2

class RoleEnum(Enum):
    USER = 0
    EMPLOYEE = 1
    ADMIN = 2

class CardTypeEnum(Enum):
    CREDITS=0
    DEBITS = 1