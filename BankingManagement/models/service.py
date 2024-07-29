import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class Service(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.ServiceName = kwargs["serviceName"] if "serviceName" in kwargs.keys() else None
        self.ServiceInfos = kwargs["serviceInfo"] if "serviceInfo" in kwargs.keys() else []

    def add_service_info(self, serviceInfo):
        self.ServiceInfos.append(serviceInfo)

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))