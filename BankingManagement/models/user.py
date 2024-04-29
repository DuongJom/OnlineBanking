import json
import os
import jwt
from time import time
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
    
