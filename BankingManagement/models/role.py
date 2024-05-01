import json
from models.base import BaseModel
from models.datetimeEncoder import DateTimeEncoder
from SysEnum import RoleType

class Role(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.RoleName = kwargs["role_name"] if "role_name" in kwargs.keys() else RoleType.USER

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))