import json

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.sex_type import SexType
from enums.collection import CollectionType

db = Database().get_db()

class User(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.USERS.value)
        
        self.name = str(kwargs["name"]).strip() if "name" in kwargs.keys() else None
        self.sex = kwargs["sex"] if "sex" in kwargs.keys() else SexType.MALE.value
        self.address_id = int(kwargs["address_id"]) if "address_id" in kwargs.keys() else None
        self.phone = str(kwargs["phone"]).strip() if "phone" in kwargs.keys() else None
        self.email = str(kwargs["email"]).strip() if "email" in kwargs.keys() else None
        self.cards = kwargs["cards"] if "cards" in kwargs.keys() else []
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))