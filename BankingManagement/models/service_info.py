import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class ServiceInfo(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        super().__init__(created_by=created_by, modified_by=modified_by)
        
        self.Content = kwargs["content"] if "content" in kwargs.keys() else None
        self.TotalAmount = kwargs["totalAmount"] if "totalAmount" in kwargs.keys() else 0.0

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
