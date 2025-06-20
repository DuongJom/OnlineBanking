import json
from datetime import datetime as dt

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.currency import CurrencyType
from enums.transaction_type import TransactionType
from enums.transaction_status import TransactionStatus
from enums.collection import CollectionType
from init_database import db

class Transaction(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.TRANSACTIONS.value)

        self.sender_id = kwargs["sender"] if "sender" in kwargs.keys() else None
        self.receiver_id = kwargs["receiver"] if "receiver" in kwargs.keys() else None
        self.message = kwargs["message"] if "message" in kwargs.keys() else None
        self.currency = kwargs["currency"] if "currency" in kwargs.keys() else CurrencyType.VND.value
        self.transaction_type = kwargs["transaction_type"] if "transaction_type" in kwargs.keys() else TransactionType.WITHDRAWAL.value
        self.amount = float(kwargs["amount"]) if "amount" in kwargs.keys() else 0
        self.status = kwargs["status"] if "status" in kwargs.keys() else TransactionStatus.SUCCESS.value
        self.current_balance = kwargs["balance"] if "balance" in kwargs.keys() else 0
        self.transaction_date = kwargs["transaction_date"] if "transaction_date" in kwargs.keys() else dt.now()

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))