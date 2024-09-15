import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class CardType(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        super().__init__(createdBy=created_by, modifiedBy=modified_by)
        
        self.TypeName = str(kwargs["typeName"]).strip() if "typeName" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))