from datetime import datetime
from  werkzeug.security import generate_password_hash
from models.base import BaseModel

class Account(BaseModel):
    def __init__(self,  AccountNumber, Branch, AccountOwner, Username, 
                 Password, LoginMethod, TransferMethod, Service):
       self.AccountNumber = AccountNumber
       self.Branch = Branch
       self.AccountOwner = AccountOwner
       self.Username = Username
       self.Password = generate_password_hash(Password)
       self.LoginMethod = LoginMethod or []
       self.TransferMethod = TransferMethod or []
       self.Service = Service or []

    def to_json(self):
        return {
            "AccountId" : self.AccountId,
            "AccountNumber" :  self.AccountNumber,
            "Branch" : self.Branch,
            "AccountOwner" : self.AccountOwner,
            "Username" : self.Username,
            "Password" : self.Password,
        }