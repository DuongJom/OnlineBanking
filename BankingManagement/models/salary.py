import json

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.employee_role_type import EmployeeRoleType

class Salary(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.BasicSalary = kwargs["basicSalary"] if "basicSalary" in kwargs.keys() else None
        self.OverTime = kwargs["overTime"] if "overTime" in kwargs.keys() else None
        self.PublicHoliday = kwargs["publicHoliday"] if "publicHoliday" in kwargs.keys() else EmployeeRoleType.NORMAL_EMPLOYEE.value
        self.ShiftAllowance = kwargs["shiftAllowance"] if "shiftAllowance" in kwargs.keys() else None
        self.GroomingAllowance = kwargs["groomingAllowance"] if "groomingAllowance" in kwargs.keys() else None
        self.PerformanceBonus = kwargs["performanceBonus"] if "performanceBonus" in kwargs.keys() else None
        self.GrossWages = kwargs["grossWages"] if "grossWages" in kwargs.keys() else None
        self.NetPay = kwargs["netPay"] if "netPay" in kwargs.keys() else None
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))

