import json
from models.base import BaseModel
from models.datetimeEncoder import DateTimeEncoder

class CardType(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.TypeName = kwargs["typeName"] if "typeName" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))