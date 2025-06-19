import json

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.mime_type import MIMEType
from enums.collection import CollectionType

db = Database().get_db()

class Attachment(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db, collection=CollectionType.ATTACHMENTS.value)
        
        self.file_name = str(kwargs['file_name']).strip() if 'file_name' in kwargs.keys() else None
        self.file_extension = self.file_name.split('.')[-1] if (self.file_name and '.' in self.file_name) else None
        self.mime_type = kwargs['mime_type'] if 'mime_type' in kwargs.keys() else MIMEType.TEXT.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))