import json
from datetime import date, timedelta

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class News(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["createdBy"] if "createdBy" in kwargs.keys() else None
        modified_by = kwargs["modifiedBy"] if "modifiedBy" in kwargs.keys() else None
        super().__init__(createdBy=created_by, modifiedBy=modified_by)
        
        self.Title = str(kwargs["title"]).strip() if "title" in kwargs.keys() else "News-{0}".format(date.today())
        self.Content = str(kwargs["content"]).strip() if "content" in kwargs.keys() else None
        self.StartDate = kwargs["startDate"] if "startDate" in kwargs.keys() else date.today()
        self.EndDate = kwargs["endDate"] if "endDate" in kwargs.keys() else (date.today() + timedelta(days=7))
        self.PublishedBy = kwargs["publishedBy"] if "publishedBy" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))