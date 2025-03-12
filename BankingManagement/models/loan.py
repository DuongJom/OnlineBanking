import json
from datetime import datetime as dt

from models.base import BaseModel
from models.database import Database
from models.datetime_encoder import DateTimeEncoder
from enums.collection import CollectionType
from enums.loan_status import LoanStatusType

db = Database().get_db()

class Loan(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=id, createdBy=created_by, modifiedBy=modified_by, database=db, collection=CollectionType.LOANS.value)

        self.Owner = int(kwargs["owner"]) if "owner" in kwargs.keys() else None
        self.Amount = float(kwargs["amount"]) if "amount" in kwargs.keys() else 0
        self.InterestRate = float(kwargs["interest_rate"]) if "interest_rate" in kwargs.keys() else 0
        self.DueDate = kwargs["due_date"] if "due_date" in kwargs.keys() else dt.now()
        self.Status = int(kwargs["status"]) if "status" in kwargs.keys() else LoanStatusType.ACTIVE.value
        self.Term = int(kwargs["term"]) if "term" in kwargs.keys() else 6
        
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))