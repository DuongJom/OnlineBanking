from models.base import BaseModel
from helpers import list_to_json

class Service(BaseModel):
    def __init__(self, ServiceName):
        super().__init__()
        self.ServiceName = ServiceName
        self.ServiceInfos = []

    def add_service_info(self, serviceInfo):
        self.ServiceInfos.append(serviceInfo)

    def to_json(self):
        return {
            "ServiceName": self.ServiceName,
            "ServiceInfos": list_to_json(self.ServiceInfos)
        }