import json
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.role_type import RoleType

class Role(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.RoleName = kwargs["role_name"] if "role_name" in kwargs.keys() else RoleType.USER

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))