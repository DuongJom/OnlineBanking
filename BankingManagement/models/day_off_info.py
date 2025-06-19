import json

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.day_off_type import DayOffType
from enums.collection import CollectionType

db = Database().get_db()

class DayOffInfo(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.DAY_OFF_INFOS.value)
        
        self.employee_id = kwargs["employee_id"] if "employee_id" in kwargs.keys() else None
        self.day = kwargs["day"] if "day" in kwargs.keys() else None
        self.month = kwargs["month"] if "month" in kwargs.keys() else None
        self.year = kwargs["year"] if "year" in kwargs.keys() else None
        self.day_off_type = kwargs["type"] if "type" in kwargs.keys() else DayOffType.UNPAID_LEAVE.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))
