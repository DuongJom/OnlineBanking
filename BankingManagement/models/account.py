import json

from  werkzeug.security import generate_password_hash

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.role_type import RoleType

class Account(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(kwargs=kwargs)
        self.AccountNumber = kwargs["accountNumber"] if "accountNumber" in kwargs.keys() else None
        self.Branch = kwargs["branch"] if "branch" in kwargs.keys() else None
        self.AccountOwner = kwargs["user"] if "user" in kwargs.keys() else None
        self.Username = str(kwargs["username"]).strip() if "username" in kwargs.keys() else None
        self.Password = generate_password_hash(kwargs["password"]) if "password" in kwargs.keys() else None
        self.Role = kwargs["role"] if "role" in kwargs.keys() else RoleType.USER.value
        self.TransferMethod = kwargs["transferMethod"] if "transferMethod" in kwargs.keys() else []
        self.LoginMethod = kwargs["loginMethod"] if "loginMethod" in kwargs.keys() else []
        self.Service = kwargs["service"] if "service" in kwargs.keys() else []
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
    


