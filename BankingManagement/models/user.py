import os
import jwt
from time import time
from base import BaseModel
class User(BaseModel):
    def __init__(self, Name, Sex, Address, Phone, Email, CardID):
        self.Name = Name
        self.Sex = Sex
        self.Address = Address
        self.Phone = Phone
        self.Email = Email
        self.CardID = CardID

    #  send the user an email that contains the JWT associated with their account
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
    
    def to_json(self):
        return {
            "Name": self.Name,
            "Sex":self.Sex,
            "Address": self.Address,
            "Phone":self.Phone,
            "Email":self.Email,
            "CardID":self.CardID
        }