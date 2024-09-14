import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class Position(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.PositionName = str(kwargs["position_name"]).strip() if "position_name" in kwargs.keys() else None
        self.AbbreviatedName = str(kwargs["abbreviated_name"]).strip() if "abbreviated_name" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))