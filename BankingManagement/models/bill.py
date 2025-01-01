import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.bill_status import BillStatusType

class Bill(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        super().__init__(createdBy=created_by, modifiedBy=modified_by)
        
        self.BillType = kwargs["type"] if "type" in kwargs.keys() else None
        self.TotalAmount = kwargs["amount"] if "amount" in kwargs.keys() else 0
        self.Status = kwargs["status"] if "status" in kwargs.keys() else BillStatusType.UNPAID.value
        self.InvoiceDate = kwargs["invoice_date"] if "invoice_date" in kwargs.keys() else None
        self.PaymentDate = kwargs["payment_date"] if "payment_date" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))