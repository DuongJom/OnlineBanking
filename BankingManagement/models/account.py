from  werkzeug.security import generate_password_hash
from models.base import BaseModel
class Account(BaseModel):
    def __init__(self, email, password, Username, AccountNumber, Branch, AccountOwner, LoginMethod, TransferMethod, Service):
        self.email = email
        self.password = generate_password_hash(password)
        self.Username = Username
        self.AccountNumber = AccountNumber
        self.Branch = Branch
        self.AccountOwner = AccountOwner
        self.LoginMethod = LoginMethod or []
        self.TransferMethod = TransferMethod or []
        self.Service = Service or []

    def to_json(self):
        return {
            "email": self.email,
            "password": self.password,
            "Username": self.Username,
            "AccountNumber": self.AccountNumber,
            "Branch": self.Branch,
            "AccountOwner": self.AccountOwner,
            "LoginMethod": self.LoginMethod,
            "TransferMethod": self.TransferMethod,
            "Service": self.Service
        }
                                    