import json

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.transfer_type import TransferType
from enums.collection import CollectionType

db = Database().get_db()

class TransferMethod(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=id, createdBy=created_by, modifiedBy=modified_by, database=db, collection=CollectionType.TRANSFER_METHODS.value)
        
        self.MethodName = kwargs["methodName"] if "methodName" in kwargs.keys() else None
        self.Value = int(kwargs["value"]) if "value" in kwargs.keys() else TransferType.SMS.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))