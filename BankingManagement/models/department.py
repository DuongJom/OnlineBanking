import json
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class Department(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.DepartmentName = kwargs["name"] if "name" in kwargs.keys() else None
        self.Manager = kwargs["manager"] if "manager" in kwargs.keys() else None
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))