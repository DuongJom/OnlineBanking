import json
from datetime import datetime as dt

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

from enums.currency import CurrencyType
from enums.transaction_type import TransactionType
from enums.transaction_status import TransactionStatus
from enums.collection import CollectionType

db = Database().get_db()

class Transaction(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=id, createdBy=created_by, modifiedBy=modified_by, database=db, collection=CollectionType.TRANSACTIONS.value)

        self.SenderId = kwargs["sender"] if "sender" in kwargs.keys() else None
        self.ReceiverId = kwargs["receiver"] if "receiver" in kwargs.keys() else None
        self.Message = kwargs["message"] if "message" in kwargs.keys() else None
        self.Currency = kwargs["currency"] if "currency" in kwargs.keys() else CurrencyType.VND.value
        self.TransactionType = kwargs["transaction_type"] if "transaction_type" in kwargs.keys() else TransactionType.WITHDRAWAL.value
        self.Amount = float(kwargs["amount"]) if "amount" in kwargs.keys() else 0
        self.Status = kwargs["status"] if "status" in kwargs.keys() else TransactionStatus.SUCCESS.value
        self.CurrentBalance = kwargs["balance"] if "balance" in kwargs.keys() else 0
        self.TransactionDate = kwargs["transactionDate"] if "transactionDate" in kwargs.keys() else dt.now()

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))