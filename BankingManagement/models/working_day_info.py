import json
from datetime import datetime, timedelta

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.working_type import WorkingType
from enums.collection import CollectionType

db = Database().get_db()

class WorkingDay(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.WORKING_DAY_INFOS.value)
        
        self.employee_id = int(kwargs['employee_id']) if 'employee_id' in kwargs.keys() else None
        self.day = kwargs['day'] if 'day' in kwargs.keys() else datetime.today().day
        self.month = kwargs['month'] if 'month' in kwargs.keys() else datetime.today().month
        self.year = kwargs['year'] if 'year' in kwargs.keys() else datetime.today().year
        self.working_status = kwargs['working_status'] if 'working_status' in kwargs.keys() else WorkingType.OFF.value
        self.check_in_time = kwargs['check_in_time'] if 'check_in_time' in kwargs.keys() else None
        self.check_out_time = kwargs['check_out_time'] if 'check_out_time' in kwargs.keys() else None
    
    def calculate_total_hours(self):
        """Calculate total hours worked based on check-in and check-out times"""
        time_diff = 0

        if self.check_in_time and self.check_out_time:
            if isinstance(self.check_in_time, str):
                self.check_in_time = datetime.strptime(self.check_in_time, '%H:%M')
            if isinstance(self.check_out_time, str):
                self.check_out_time = datetime.strptime(self.check_out_time, '%H:%M')
            
            # Handle cases where check-out is on the next day
            if self.check_out_time < self.check_in_time:
                self.check_out_time += timedelta(days=1)
            
            time_diff = self.check_out_time - self.check_in_time
        return round(time_diff.total_seconds() / 3600, 2)
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))