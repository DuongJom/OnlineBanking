import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.day_off_type import DayOffType

class DayOffInfo(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        super().__init__(createdBy=created_by, modifiedBy=modified_by)
        
        self.EmployeeId = kwargs["employeeId"] if "employeeId" in kwargs.keys() else None
        self.Day = kwargs["day"] if "day" in kwargs.keys() else None
        self.Month = kwargs["month"] if "month" in kwargs.keys() else None
        self.Year = kwargs["year"] if "year" in kwargs.keys() else None
        self.DayOffType = kwargs["type"] if "type" in kwargs.keys() else DayOffType.UNPAID_LEAVE.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
