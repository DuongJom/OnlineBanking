import json
from models.base import BaseModel
from models.datetimeEncoder import DateTimeEncoder

class Address(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.Street = kwargs["street"] if "street" in kwargs.keys() else None
        self.City = kwargs["city"] if "city" in kwargs.keys() else None
        self.Ward = kwargs["ward"] if "ward" in kwargs.keys() else None
        self.Country = kwargs["country"] if "country" in kwargs.keys() else None
        self.District = kwargs["district"] if "district" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))