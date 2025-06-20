import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.collection import CollectionType
from init_database import db

class Branch(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.BRANCHES.value)
        
        self.branch_name = str(kwargs["branch_name"]).strip() if "branch_name" in kwargs.keys() else None
        self.address = str(kwargs["address"]).strip() if "address" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
