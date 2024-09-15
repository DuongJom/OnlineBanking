import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class Role(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        super().__init__(createdBy=created_by, modifiedBy=modified_by)

        self.Value = kwargs["value"] if "value" in kwargs.keys() else None
        self.RoleName = str(kwargs["roleName"]).strip()

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))