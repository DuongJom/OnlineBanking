import json

from models.base import BaseModel
from models.database import Database
from models.datetime_encoder import DateTimeEncoder
from enums.bill_status import BillStatusType
from enums.collection import CollectionType

db = Database().get_db()

class Bill(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db, collection=CollectionType.BILLS.value)

        self.account_id = kwargs["account_id"] if "account_id" in kwargs.keys() else None
        self.bill_type = kwargs["type"] if "type" in kwargs.keys() else None
        self.total_amount = kwargs["amount"] if "amount" in kwargs.keys() else 0
        self.status = kwargs["status"] if "status" in kwargs.keys() else BillStatusType.UNPAID.value
        self.invoice_date = kwargs["invoice_date"] if "invoice_date" in kwargs.keys() else None
        self.payment_date = kwargs["payment_date"] if "payment_date" in kwargs.keys() else None
        self.payment_method = kwargs["payment_method"] if "payment_method" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))