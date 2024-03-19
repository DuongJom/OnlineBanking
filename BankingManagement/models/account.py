from models.base import BaseModel
from helpers import list_to_json
class Account(BaseModel):
    def __init__(self, AccountNumber, Branch, AccountOwner, Username, Password,
                 LoginMethod, TransferMethod, Service):
        super().__init__()
        self.AccountNumber = AccountNumber
        self.Branch = Branch or None
        self.AccountOwner = AccountOwner or None
        self.Username = Username
        self.Password = Password
        self.TransferMethod = TransferMethod or []
        self.LoginMethod = LoginMethod or []
        self.Service = Service or []
    
    def to_json(self):
        return {
            "AccountNumber": self.AccountNumber,
            "Branch": self.Branch.to_json(),
            "AccountOwner": self.AccountOwner.to_json(),
            "UserName": self.UserName,
            "Password": self.Password,
            "TransferMethod": list_to_json(self.TransferMethod),
            "LoginMethod": list_to_json(self.LoginMethod),
            "Service": list_to_json(self.Service)
        }