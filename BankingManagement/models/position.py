import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class Position(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        super().__init__(created_by=created_by, modified_by=modified_by)
        
        self.PositionName = str(kwargs["position_name"]).strip() if "position_name" in kwargs.keys() else None
        self.AbbreviatedName = str(kwargs["abbreviated_name"]).strip() if "abbreviated_name" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))