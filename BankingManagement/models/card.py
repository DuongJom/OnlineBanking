import json
from datetime import datetime as dt, timedelta

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.collection import CollectionType
from enums.card_type import CardType
from init_database import db

class Card(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.CARDS.value)
        
        self.card_number = kwargs["card_number"] if "card_number" in kwargs.keys() else None
        self.cvv_number = kwargs["cvv_number"] if "cvv_number" in kwargs.keys() else None
        self.expired_date = kwargs["expired_date"] if "expired_date" in kwargs.keys() else (dt.today() + timedelta(days=365*3))
        self.issuance_date = kwargs["issuance_date"] if "issuance_date" in kwargs.keys() else dt.today()
        self.type = kwargs["type"] if "type" in kwargs.keys() else CardType.CREDITS.value
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
