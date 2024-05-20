import json
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.mime_type import MIMEType

class Attachment(BaseModel):
    def __init__(self, **kwargs):
        self.FileName = kwargs['fileName'] if 'fileName' in kwargs.keys() else None
        self.Extension = self.FileName.split('.')[-1] if (not self.FileName and self.FileName.contains('.')) else None
        self.MIMEType = kwargs['mimeType'] if 'mimeType' in kwargs.keys() else MIMEType.TEXT.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))