import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class ServiceInfo(BaseModel):
    def __init__(self, **kwargs):
        super.__init__()
        self.Content = kwargs["content"] if "content" in kwargs.keys() else None
        self.TotalAmount = kwargs["totalAmount"] if "totalAmount" in kwargs.keys() else 0.0

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
