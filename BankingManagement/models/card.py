import json

from datetime import datetime as dt, timedelta
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class Card(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        super().__init__(created_by=created_by, modified_by=modified_by)
        
        self.CardNumber = kwargs["cardNumber"] if "cardNumber" in kwargs.keys() else None
        self.CVV = kwargs["cvv"] if "cvv" in kwargs.keys() else None
        self.ExpiredDate = kwargs["expiredDate"] if "expiredDate" in kwargs.keys() else (dt.today() + timedelta(days=365*3))
        self.IssuanceDate = kwargs["issuanceDate"] if "issuanceDate" in kwargs.keys() else dt.today()
        self.Type = kwargs["type"] if "type" in kwargs.keys() else []
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
