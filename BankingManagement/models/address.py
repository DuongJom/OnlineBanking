import json

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.collection import CollectionType

db = Database().get_db()

class Address(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=id, createdBy=created_by, modifiedBy=modified_by, database=db, collection=CollectionType.ADDRESSES.value)
        
        self.Street = str(kwargs["street"]).strip() if "street" in kwargs.keys() else None
        self.City = str(kwargs["city"]).strip() if "city" in kwargs.keys() else None
        self.Ward = str(kwargs["ward"]).strip() if "ward" in kwargs.keys() else None
        self.Country = str(kwargs["country"]).strip() if "country" in kwargs.keys() else None
        self.District = str(kwargs["district"]).strip() if "district" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))