import json
from models.base import BaseModel
from models.datetimeEncoder import DateTimeEncoder

class Branch(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.BranchName = kwargs["branchName"] if "branchName" in kwargs.keys() else None
        self.Address = kwargs["address"] if "address" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
