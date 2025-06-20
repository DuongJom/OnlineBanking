import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.employee_role_type import EmployeeRoleType
from enums.collection import CollectionType
from init_database import db

class Employee(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.EMPLOYEES.value)
        
        self.employee_name = str(kwargs["employee_name"]).strip() if "employee_name" in kwargs.keys() else None
        self.position = kwargs["position"] if "position" in kwargs.keys() else None
        self.role = kwargs["role"] if "role" in kwargs.keys() else EmployeeRoleType.NORMAL_EMPLOYEE.value
        self.sex = kwargs["sex"] if "sex" in kwargs.keys() else None
        self.phone = str(kwargs["phone"]).strip() if "phone" in kwargs.keys() else None
        self.email = str(kwargs["email"]).strip() if "email" in kwargs.keys() else None
        self.address = str(kwargs["address"]).strip() if "address" in kwargs.keys() else None
        self.working_days = kwargs["working_days"] if "working_days" in kwargs.keys() else []
        self.day_offs = kwargs["day_offs"] if "day_offs" in kwargs.keys() else []
        self.salary = kwargs["salary"] if "salary" in kwargs.keys() else None
        
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))

