import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class Service(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        super().__init__(created_by=created_by, modified_by=modified_by)
        
        self.ServiceName = kwargs["serviceName"] if "serviceName" in kwargs.keys() else None
        self.ServiceInfos = kwargs["serviceInfo"] if "serviceInfo" in kwargs.keys() else []

    def add_service_info(self, serviceInfo):
        self.ServiceInfos.append(serviceInfo)

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))