import json

from datetime import datetime

from models.database import Database
from enums.deleted_type import DeletedType
from models.datetime_encoder import DateTimeEncoder
from helpers import get_max_id

class BaseModel:
    def __init__(self, **kwargs):
        self.CreatedDate = datetime.now()
        self.CreatedBy = str(kwargs['createdBy']) if 'createdBy' in kwargs.keys() else None
        self.ModifiedDate = datetime.now()
        self.ModifiedBy = str(kwargs['modifiedBy']) if 'modifiedBy' in kwargs.keys() else None
        self.IsDeleted = DeletedType.AVAILABLE.value
        self.Database = kwargs['database'] if 'database' in kwargs.keys() else Database().get_db()
        self.CollectionName = str(kwargs['collection'])
        self._id = int(kwargs['id']) if 'id' in kwargs.keys() else get_max_id(self.Database, self.CollectionName)

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))