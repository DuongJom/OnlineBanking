import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.transfer_type import TransferType
from enums.collection import CollectionType
from init_database import db

class TransferMethod(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.TRANSFER_METHODS.value)
        
        self.method_name = kwargs["method_name"] if "method_name" in kwargs.keys() else None
        self.value = int(kwargs["value"]) if "value" in kwargs.keys() else TransferType.SMS.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))