import json
from models.base import BaseModel
from models.datetimeEncoder import DateTimeEncoder

class Card(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.CardNumber = kwargs["cardNumber"] if "cardNumber" in kwargs.keys() else None
        self.CVV = kwargs["cvv"] if "cvv" in kwargs.keys() else None
        self.ExpiredDate = kwargs["expiredDate"] if "expiredDate" in kwargs.keys() else None
        self.IssuanceDate = kwargs["issuanceDate"] if "issuanceDate" in kwargs.keys() else None
        self.Type = kwargs["type"] if "type" in kwargs.keys() else []
    
    def to_json(self):
        return json.dumps(self.__dict__, cls=DateTimeEncoder)
