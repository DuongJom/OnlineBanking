import json
from models.base import BaseModel
from models.datetimeEncoder import DateTimeEncoder

class Role(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.RoleName = kwargs["role_name"] if "role_name" in kwargs.keys() else None

    def to_json(self):
        return json.dumps(self.__dict__, cls=DateTimeEncoder)