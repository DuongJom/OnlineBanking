import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.collection import CollectionType
from init_database import db

class Address(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db, collection=CollectionType.ADDRESSES.value)
        
        self.street = str(kwargs["street"]).strip() if "street" in kwargs.keys() else None
        self.city = str(kwargs["city"]).strip() if "city" in kwargs.keys() else None
        self.ward = str(kwargs["ward"]).strip() if "ward" in kwargs.keys() else None
        self.country = str(kwargs["country"]).strip() if "country" in kwargs.keys() else None
        self.district = str(kwargs["district"]).strip() if "district" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))