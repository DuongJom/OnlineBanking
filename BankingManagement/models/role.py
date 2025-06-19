import json

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.collection import CollectionType

db = Database().get_db()

class Role(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.ROLES.value)

        self.value = kwargs["value"] if "value" in kwargs.keys() else None
        self.role_name = str(kwargs["role_name"]).strip()

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))