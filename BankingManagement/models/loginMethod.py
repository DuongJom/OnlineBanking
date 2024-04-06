import json
from models.base import BaseModel
from models.datetimeEncoder import DateTimeEncoder

class LoginMethod(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.MethodName = kwargs["methodName"] if "methodName" in kwargs.keys() else None

    def to_json(self):
        return json.dumps(self.__dict__, cls=DateTimeEncoder)