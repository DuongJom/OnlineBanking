from base import BaseModel
class User(BaseModel):
    def __init__(self, Name, Sex, Address, Phone, Email, CardID):
        self.Name = Name
        self.Sex = Sex
        self.Address = Address
        self.Phone = Phone
        self.Email = Email
        self.CardID = CardID

    def to_json(self):
        return {
            "Name": self.Name,
            "Sex":self.Sex,
            "Address": self.Address,
            "Phone":self.Phone,
            "Email":self.Email,
            "CardID":self.CardID
        }
