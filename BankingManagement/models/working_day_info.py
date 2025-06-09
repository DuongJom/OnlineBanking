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
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=id, createdBy=created_by, modifiedBy=modified_by, database=db, collection=CollectionType.WORKING_DAY_INFOS.value)
        
        self.EmployeeId = int(kwargs['emp_id']) if 'emp_id' in kwargs.keys() else None
        self.Day = kwargs['day'] if 'day' in kwargs.keys() else datetime.today().day
        self.Month = kwargs['month'] if 'month' in kwargs.keys() else datetime.today().month
        self.Year = kwargs['year'] if 'year' in kwargs.keys() else datetime.today().year
        self.WorkingStatus = kwargs['workingStatus'] if 'workingStatus' in kwargs.keys() else WorkingType.OFF.value
        self.CheckIn = kwargs['checkIn'] if 'checkIn' in kwargs.keys() else None
        self.CheckOut = kwargs['checkOut'] if 'checkOut' in kwargs.keys() else None
        self.TotalHours = kwargs['totalHours'] if 'totalHours' in kwargs.keys() else 0
    
    def calculate_total_hours(self):
        """Calculate total hours worked based on check-in and check-out times"""
        if self.CheckIn and self.CheckOut:
            if isinstance(self.CheckIn, str):
                self.CheckIn = datetime.strptime(self.CheckIn, '%H:%M')
            if isinstance(self.CheckOut, str):
                self.CheckOut = datetime.strptime(self.CheckOut, '%H:%M')
            
            # Handle cases where check-out is on the next day
            if self.CheckOut < self.CheckIn:
                self.CheckOut += timedelta(days=1)
            
            time_diff = self.CheckOut - self.CheckIn
            self.TotalHours = round(time_diff.total_seconds() / 3600, 2)
        return self.TotalHours
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))