import json
from datetime import date, timedelta

from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder

class News(BaseModel):
    def __init__(self, **kwargs):
        self.Title = kwargs["title"] if "title" in kwargs.keys() else "News-{0}".format(date.today())
        self.Content = kwargs["content"] if "content" in kwargs.keys() else None
        self.StartDate = kwargs["start_date"] if "start_date" in kwargs.keys() else date.today()
        self.EndDate = kwargs["end_date"] if "end_date" in kwargs.keys() else (date.today() + timedelta(days=7))
        self.PublishedBy = kwargs["published_by"] if "published_by" in kwargs.keys() else None

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))