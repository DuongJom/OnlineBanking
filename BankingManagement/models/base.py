import json
from datetime import datetime

from enums.deleted_type import DeletedType
from models.datetime_encoder import DateTimeEncoder
from helpers.helpers import get_max_id
from init_database import db

class BaseModel:
    def __init__(self, **kwargs):
        self.created_date = datetime.now()
        self.created_by = kwargs['created_by'] if 'created_by' in kwargs.keys() else None
        self.modified_date = datetime.now()
        self.modified_by = kwargs['modified_by'] if 'modified_by' in kwargs.keys() else None
        self.is_deleted = DeletedType.AVAILABLE.value
        self.database = kwargs['database'] if 'database' in kwargs.keys() else db
        self.collection_name = str(kwargs['collection'])
        self._id = int(kwargs['id']) if 'id' in kwargs.keys() else get_max_id(self.database, self.collection_name)

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))