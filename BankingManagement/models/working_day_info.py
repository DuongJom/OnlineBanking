import json

from datetime import datetime

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.working_type import WorkingType

class WorkingDay(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        super().__init__(created_by=created_by, modified_by=modified_by)
        
        self.Day = kwargs['day'] if 'day' in kwargs.keys() else datetime.today().day
        self.Month = kwargs['month'] if 'month' in kwargs.keys() else datetime.today().month
        self.Year = kwargs['year'] if 'year' in kwargs.keys() else datetime.today().year
        self.WorkingStatus = kwargs['workingStatus'] if 'workingStatus' in kwargs.keys() else WorkingType.OFF.value
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))