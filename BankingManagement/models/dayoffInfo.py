import json
from models.base import BaseModel
from models.datetimeEncoder import DateTimeEncoder

class DayOffInfo(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.Day = kwargs["day"] if "day" in kwargs.keys() else None
        self.Month = kwargs["month"] if "month" in kwargs.keys() else None
        self.Year = kwargs["year"] if "year" in kwargs.keys() else None
        self.DayOffType = kwargs["type"] if "type" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
