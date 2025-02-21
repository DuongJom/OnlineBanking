import json

from datetime import datetime

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
        
        self.Day = kwargs['day'] if 'day' in kwargs.keys() else datetime.today().day
        self.Month = kwargs['month'] if 'month' in kwargs.keys() else datetime.today().month
        self.Year = kwargs['year'] if 'year' in kwargs.keys() else datetime.today().year
        self.WorkingStatus = kwargs['workingStatus'] if 'workingStatus' in kwargs.keys() else WorkingType.OFF.value
    
    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))