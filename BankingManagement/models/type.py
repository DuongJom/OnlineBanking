import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class Type(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        super().__init__(createdBy=created_by, modifiedBy=modified_by)
        
        self.TypeName = kwargs["typeName"] if "typeName" in kwargs.keys() else None
        self.TypeValue = kwargs["typeValue"] if "typeValue" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))