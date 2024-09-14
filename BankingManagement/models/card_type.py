import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class CardType(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.TypeName = str(kwargs["typeName"]).strip() if "typeName" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))