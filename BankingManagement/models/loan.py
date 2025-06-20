import json
from datetime import datetime as dt

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.collection import CollectionType
from enums.loan_status import LoanStatusType
from enums.expired_time_loan import ExpiredTimeLoan
from init_database import db

class Loan(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.LOANS.value)

        self.owner = int(kwargs["owner"]) if "owner" in kwargs.keys() else None
        self.amount = float(kwargs["amount"]) if "amount" in kwargs.keys() else 0
        self.interest_rate = float(kwargs["interest_rate"]) if "interest_rate" in kwargs.keys() else 0
        self.due_date = kwargs["due_date"] if "due_date" in kwargs.keys() else dt.now()
        self.status = int(kwargs["status"]) if "status" in kwargs.keys() else LoanStatusType.ACTIVE.value
        self.term = int(kwargs["term"]) if "term" in kwargs.keys() else ExpiredTimeLoan.SIX_MONTH.value
        
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))