import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class Address(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.Street = str(kwargs["street"]).strip() if "street" in kwargs.keys() else None
        self.City = str(kwargs["city"]).strip() if "city" in kwargs.keys() else None
        self.Ward = str(kwargs["ward"]).strip() if "ward" in kwargs.keys() else None
        self.Country = str(kwargs["country"]).strip() if "country" in kwargs.keys() else None
        self.District = str(kwargs["district"]).strip() if "district" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))