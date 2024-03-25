from models.base import BaseModel

class User(BaseModel):
    def __init__(self, Name=None, Sex=None, Address=None, Phone=None, Email=None, CardID=None):
        self.Name = Name
        self.Sex = Sex
        self.Address = Address
        self.Phone = Phone
        self.Email = Email
        self.CardID = CardID

    def to_json(self):
        return {
            "Name" : self.Name,
            "Sex" : self.Sex,
            "Address" : self.Address,
            "Phone" : self.Phone,
            "Email" : self.Email,
            "CardID" : self.CardID,
            "CreatedDate" : self.CreatedDate,
            "CreatedBy" : self.CreatedBy,
            "ModifiedDate" : self.ModifiedDate,
            "ModifiedBy" : self.ModifiedBy
        }
    
