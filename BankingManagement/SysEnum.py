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

class WorkingType(Enum):
    OFF  = 0
    WFH = 1
    WORK_IN_COMPANY = 2

class DayOffType(Enum):
    HALF_DAY = 0
    VACATION = 1
    WEDDING = 2
    SICK = 3
    OTHER = 4