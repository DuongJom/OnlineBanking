import json
from models.base import BaseModel
from models.datetimeEncoder import DateTimeEncoder

class Position(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.PositionName = kwargs["position_name"] if "position_name" in kwargs.keys() else None
        self.AbbreviatedName = kwargs["abbreviated_name"] if "abbreviated_name" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))