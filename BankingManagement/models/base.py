import json

from datetime import datetime

from enums.deleted_type import DeletedType
from models.datetime_encoder import DateTimeEncoder
class BaseModel:
    def __init__(self, **kwargs):
        self.CreatedDate = datetime.now()
        self.CreatedBy = kwargs['createdBy'] if 'createdBy' in kwargs.keys() else None
        self.ModifiedDate = datetime.now()
        self.ModifiedBy = kwargs['modifiedBy'] if 'modifiedBy' in kwargs.keys() else None
        self.IsDeleted = DeletedType.AVAILABLE.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))