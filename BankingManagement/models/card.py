import json
from datetime import datetime as dt, timedelta

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.collection import CollectionType
from enums.card_type import CardType

db = Database().get_db()

class Card(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=id, createdBy=created_by, modifiedBy=modified_by, database=db, collection=CollectionType.CARDS.value)
        
        self.CardNumber = kwargs["cardNumber"] if "cardNumber" in kwargs.keys() else None
        self.CVV = kwargs["cvv"] if "cvv" in kwargs.keys() else None
        self.ExpiredDate = kwargs["expiredDate"] if "expiredDate" in kwargs.keys() else (dt.today() + timedelta(days=365*3))
        self.IssuanceDate = kwargs["issuanceDate"] if "issuanceDate" in kwargs.keys() else dt.today()
        self.Type = kwargs["type"] if "type" in kwargs.keys() else CardType.CREDITS.value
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
