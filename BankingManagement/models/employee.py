import json
from models.base import BaseModel
from models.datetimeEncoder import DateTimeEncoder

class Employee(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.EmployeeName = kwargs["employeeName"] if "employeeName" in kwargs.keys() else None
        self.Sex = kwargs["sex"] if "sex" in kwargs.keys() else None
        self.Phone = kwargs["phone"] if "phone" in kwargs.keys() else None
        self.Email = kwargs["email"] if "email" in kwargs.keys() else None
        self.Address = kwargs["address"] if "address" in kwargs.keys() else None
        self.Check_in_time = kwargs["checkIn"] if "checkIn" in kwargs.keys() else None
        self.Check_out_time = kwargs["checkOut"] if "checkOut" in kwargs.keys() else None
        self.Working_status = kwargs["workingStatus"] if "workingStatus" in kwargs.keys() else None
        self.Working_days = kwargs["workingDays"] if "workingDays" in kwargs.keys() else []
        self.DayOffs = kwargs["dayOffs"] if "dayOffs" in kwargs.keys else []
        self.Salary = kwargs["salary"] if "salary" in kwargs.keys() else None
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))


