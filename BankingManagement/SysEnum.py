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

class CardType(Enum):
    CREDITS=0
    DEBITS = 1
class WorkingType(Enum):
    OFF  = 0
    HALF_DAY = 1
    VACATION = 2
    WEDDING = 3
    SICK = 4
    WFH = 5
    WORK_IN_COMPANY = 6
    OTHER = 7

class DayOffType(Enum):
    PAID_LEAVE = 0
    UNPAID_LEAVE = 1

class MIMEType(Enum):
    TEXT = 0
    PDF = 1
    EXCEL_XLS = 2
    EXCEL_XLSX = 3
    EXCEL_XLSM = 4
    XML = 5
    WORD_DOC = 6
    WORD_DOT = 7
    WORD_DOCX = 8
    WORD_DOTX = 9
    IMG_PNG = 10
    IMG_JPG = 11
    IMG_BMP = 12
    HTML = 13
    AUDIO = 14
    VIDEO = 15

