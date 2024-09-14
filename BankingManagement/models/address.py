import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class Address(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        super().__init__(created_by=created_by, modified_by=modified_by)
        
        self.Street = str(kwargs["street"]).strip() if "street" in kwargs.keys() else None
        self.City = str(kwargs["city"]).strip() if "city" in kwargs.keys() else None
        self.Ward = str(kwargs["ward"]).strip() if "ward" in kwargs.keys() else None
        self.Country = str(kwargs["country"]).strip() if "country" in kwargs.keys() else None
        self.District = str(kwargs["district"]).strip() if "district" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))