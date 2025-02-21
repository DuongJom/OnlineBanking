import json

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.employee_role_type import EmployeeRoleType
from enums.collection import CollectionType

db = Database().get_db()

class Employee(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=id, createdBy=created_by, modifiedBy=modified_by, database=db, collection=CollectionType.EMPLOYEES.value)
        
        self.EmployeeName = str(kwargs["employeeName"]).strip() if "employeeName" in kwargs.keys() else None
        self.Position = kwargs["position"] if "position" in kwargs.keys() else None
        self.Role = kwargs["role"] if "role" in kwargs.keys() else EmployeeRoleType.NORMAL_EMPLOYEE.value
        self.Sex = kwargs["sex"] if "sex" in kwargs.keys() else None
        self.Phone = str(kwargs["phone"]).strip() if "phone" in kwargs.keys() else None
        self.Email = str(kwargs["email"]).strip() if "email" in kwargs.keys() else None
        self.Address = str(kwargs["address"]).strip() if "address" in kwargs.keys() else None
        self.Check_in_time = kwargs["checkIn"] if "checkIn" in kwargs.keys() else None
        self.Check_out_time = kwargs["checkOut"] if "checkOut" in kwargs.keys() else None
        self.Working_status = kwargs["workingStatus"] if "workingStatus" in kwargs.keys() else None
        self.Working_days = kwargs["workingDays"] if "workingDays" in kwargs.keys() else []
        self.DayOffs = kwargs["dayOffs"] if "dayOffs" in kwargs.keys else []
        self.Salary = kwargs["salary"] if "salary" in kwargs.keys() else None
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))

