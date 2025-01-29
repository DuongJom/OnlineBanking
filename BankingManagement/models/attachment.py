import json

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.mime_type import MIMEType
from enums.collection import CollectionType

db = Database().get_db()

class Attachment(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=id, createdBy=created_by, modifiedBy=modified_by, database=db, collection=CollectionType.ATTACHMENTS.value)
        
        self.FileName = str(kwargs['fileName']).strip() if 'fileName' in kwargs.keys() else None
        self.Extension = self.FileName.split('.')[-1] if (not self.FileName and self.FileName.contains('.')) else None
        self.MIMEType = kwargs['mimeType'] if 'mimeType' in kwargs.keys() else MIMEType.TEXT.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))