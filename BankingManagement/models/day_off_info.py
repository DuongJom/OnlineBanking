import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.day_off_type import DayOffType

class DayOffInfo(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.Day = kwargs["day"] if "day" in kwargs.keys() else None
        self.Month = kwargs["month"] if "month" in kwargs.keys() else None
        self.Year = kwargs["year"] if "year" in kwargs.keys() else None
        self.DayOffType = kwargs["type"] if "type" in kwargs.keys() else DayOffType.UNPAID_LEAVE.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
