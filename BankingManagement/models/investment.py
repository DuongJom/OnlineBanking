import json
from datetime import datetime as dt

from models.base import BaseModel
from models.database import Database
from models.datetime_encoder import DateTimeEncoder
from enums.investment_status import InvestmentStatus
from enums.collection import CollectionType

db = Database().get_db()

class Investment(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=id, createdBy=created_by, modifiedBy=modified_by, database=db, collection=CollectionType.ACCOUNTS.value)

        self.Owner = kwargs['owner'] if 'owner' in kwargs.keys() else None
        self.Name = kwargs['name'] if 'name' in kwargs.keys() else None
        self.Type = kwargs['type'] if 'type' in kwargs.keys() else None
        self.InvestmentAmount = float(kwargs['investment_amount']) if 'investment_amount' in kwargs.keys() else 0
        self.CurrentAmount = float(kwargs['current_amount']) if 'current_amount' in kwargs.keys() else 0
        self.CurrentRate = float(kwargs['rate']) if 'rate' in kwargs.keys() else 0
        self.InvestmentDate = kwargs['investment_date'] if 'investment_date' in kwargs.keys() else dt.now()
        self.Status = int(kwargs['status']) if 'status' in kwargs.keys() else InvestmentStatus.IN_PROCESSING.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))