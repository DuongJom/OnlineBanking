from datetime import datetime

class User:
    def __init__(self, Name, Sex, Address, Phone, Email, CardID, CreatedDate):
        self.Name = Name
        self.Sex = Sex
        self.Address = Address
        self.Phone = Phone
        self.Email = Email
        self.CardID = CardID
        self.CreatedDate = datetime.utcnow()
        self.CreatedBy = None
        self.ModifiedDate = None
        self.MofifiedBy = None

    def to_json(self):
        return {
             "UserId" : self.UserId,
             "Name" : self.Name,
             "Sex" : self.Sex,
             "Address" : self.Address
        }
