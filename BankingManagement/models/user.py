import json
from models.base import BaseModel
from models.datetimeEncoder import DateTimeEncoder

class User(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.Name = kwargs["name"] if "name" in kwargs.keys() else None
        self.Sex = kwargs["sex"] if "sex" in kwargs.keys() else 0
        self.Address = kwargs["address"] if "address" in kwargs.keys() else None
        self.Phone = kwargs["phone"] if "phone" in kwargs.keys() else None
        self.Email = kwargs["email"] if "email" in kwargs.keys() else None
        self.Card = kwargs["card"] if "card" in kwargs.keys() else []
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
