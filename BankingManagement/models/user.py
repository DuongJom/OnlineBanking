from models.base import BaseModel
from helpers import list_to_json

class User(BaseModel):
    def __init__(self, Name, Sex, Address, Phone, Email, Card):
        super().__init__()
        self.Name = Name
        self.Sex = Sex
        self.Address = Address
        self.Phone = Phone
        self.Email = Email
        self.Card = Card or []
    
    def to_json(self):
        return {
            "Name": self.Name,
            "Sex": self.Sex,
            "Address": self.Address.to_json(),
            "Phone": self.Phone,
            "Email": self.Email,
            "Card": list_to_json(self.Card),
            "CreatedDate" : self.CreatedDate,
            "CreatedBy" : self.CreatedBy,
            "ModifiedDate" : self.ModifiedDate,
            "ModifiedBy" : self.ModifiedBy
        }
