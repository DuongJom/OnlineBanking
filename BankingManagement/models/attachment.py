import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.mime_type import MIMEType

class Attachment(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        super().__init__(created_by=created_by, modified_by=modified_by)
        
        self.FileName = str(kwargs['fileName']).strip() if 'fileName' in kwargs.keys() else None
        self.Extension = self.FileName.split('.')[-1] if (not self.FileName and self.FileName.contains('.')) else None
        self.MIMEType = kwargs['mimeType'] if 'mimeType' in kwargs.keys() else MIMEType.TEXT.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))