import json

from  werkzeug.security import generate_password_hash
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.role_type import RoleType
from enums.currency import CurrencyType
from enums.collection import CollectionType
from init_database import db

class Account(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db, collection=CollectionType.ACCOUNTS.value)
        
        self.account_number = kwargs["account_number"] if "account_number" in kwargs.keys() else None
        self.branch_id = kwargs["branch"] if "branch" in kwargs.keys() else None
        self.account_owner = kwargs["user"] if "user" in kwargs.keys() else None
        self.balance = float(kwargs["balance"]) if "balance" in kwargs.keys() else 0
        self.currency = kwargs["currency"] if "currency" in kwargs.keys() else CurrencyType.VND.value
        self.username = str(kwargs["username"]).strip() if "username" in kwargs.keys() else None
        self.password = generate_password_hash(kwargs["password"], method='pbkdf2:sha256', salt_length=16) if "password" in kwargs.keys() else None
        self.role = int(kwargs["role"]) if "role" in kwargs.keys() else RoleType.USER.value
        self.transfer_method = kwargs["transfer_method"] if "transfer_method" in kwargs.keys() else []
        self.login_method = kwargs["login_method"] if "login_method" in kwargs.keys() else []
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
    


