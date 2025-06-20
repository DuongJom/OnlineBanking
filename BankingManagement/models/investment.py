import json
from datetime import datetime as dt

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.investment_status import InvestmentStatus
from enums.collection import CollectionType
from init_database import db

class Investment(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.INVESTMENTS_SAVINGS.value)

        self.owner = kwargs['owner'] if 'owner' in kwargs.keys() else None
        self.name = kwargs['name'] if 'name' in kwargs.keys() else None
        self.type = kwargs['type'] if 'type' in kwargs.keys() else None
        self.investmentAmount = float(kwargs['investment_amount']) if 'investment_amount' in kwargs.keys() else 0
        self.current_amount = float(kwargs['current_amount']) if 'current_amount' in kwargs.keys() else 0
        self.current_rate = float(kwargs['current_rate']) if 'current_rate' in kwargs.keys() else 0
        self.investment_date = kwargs['investment_date'] if 'investment_date' in kwargs.keys() else dt.now()
        self.status = int(kwargs['status']) if 'status' in kwargs.keys() else InvestmentStatus.IN_PROCESSING.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))