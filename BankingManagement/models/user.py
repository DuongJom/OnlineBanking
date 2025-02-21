import json, os, jwt

from time import time

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.sex_type import SexType
from enums.collection import CollectionType

db = Database().get_db()

class User(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=id, createdBy=created_by, modifiedBy=modified_by, database=db, collection=CollectionType.USERS.value)
        
        self.Name = str(kwargs["name"]).strip() if "name" in kwargs.keys() else None
        self.Sex = kwargs["sex"] if "sex" in kwargs.keys() else SexType.MALE.value
        self.Address = kwargs["address"] if "address" in kwargs.keys() else None
        self.Phone = str(kwargs["phone"]).strip() if "phone" in kwargs.keys() else None
        self.Email = str(kwargs["email"]).strip() if "email" in kwargs.keys() else None
        self.Card = kwargs["card"] if "card" in kwargs.keys() else []
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
    
    #send the user an email that contains the JWT associated with their account
    def get_reset_token(self, expires=500):
        return jwt.encode({'reset_password': self.username,
                           'exp':    time() + expires},
                           key=os.getenv('SECRET_KEY_FLASK'))
    
    def verify_reset_token(self,token):
        try:
            username = jwt.decode(token, key=os.getenv('SECRET_KEY_FLASK'))['reset_password']
            print(username)
        except Exception as e:
            print(e)
            return
        return User
    
