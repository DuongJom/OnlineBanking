import json

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.collection import CollectionType

db = Database().get_db()

class CardType(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=id, createdBy=created_by, modifiedBy=modified_by, database=db, collection=CollectionType.CARD_TYPES.value)
        
        self.TypeName = kwargs["typeName"] if "typeName" in kwargs.keys() else None
        self.TypeValue = kwargs["typeValue"] if "typeValue" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))