import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class Branch(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.BranchName = str(kwargs["branchName"]).strip() if "branchName" in kwargs.keys() else None
        self.Address = str(kwargs["address"]).strip() if "address" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
