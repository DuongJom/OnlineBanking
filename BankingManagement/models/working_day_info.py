import json

from datetime import datetime

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.working_type import WorkingType

class WorkingDay(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.Day = kwargs['day'] if 'day' in kwargs.keys() else datetime.today().day
        self.Month = kwargs['month'] if 'month' in kwargs.keys() else datetime.today().month
        self.Year = kwargs['year'] if 'year' in kwargs.keys() else datetime.today().year
        self.WorkingStatus = kwargs['workingStatus'] if 'workingStatus' in kwargs.keys() else WorkingType.OFF.value
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))