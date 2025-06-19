import json
from datetime import date, timedelta

from models.database import Database
from models.base import BaseModel
from models.datetime_encoder import DateTimeEncoder
from enums.collection import CollectionType
from enums.news_type import NewsType
from enums.news_read_status import NewsReadStatusType

db = Database().get_db()

class News(BaseModel):
    def __init__(self, **kwargs):
        created_by = kwargs["created_by"] if "created_by" in kwargs.keys() else None
        modified_by = kwargs["modified_by"] if "modified_by" in kwargs.keys() else None
        model_id = kwargs["id"] if "id" in kwargs.keys() else None
        super().__init__(id=model_id, created_by=created_by, modified_by=modified_by, database=db,
                         collection=CollectionType.NEWS.value)
        
        self.title = str(kwargs["title"]).strip() if "title" in kwargs.keys() else "News-{0}".format(date.today())
        self.content = str(kwargs["content"]).strip() if "content" in kwargs.keys() else None
        self.start_date = kwargs["start_date"] if "start_date" in kwargs.keys() else date.today()
        self.end_date = kwargs["end_date"] if "end_date" in kwargs.keys() else (date.today() + timedelta(days=7))
        self.published_by = kwargs["published_by"] if "published_by" in kwargs.keys() else None
        self.type = int(kwargs["type"]) if "type" in kwargs.keys() else NewsType.NEW.value
        self.read_status = int(kwargs["read_status"]) if "read_status" in kwargs.keys() else NewsReadStatusType.UNREAD.value

    def to_json(self):
        return json.loads(json.dumps(self.__dict__, cls=DateTimeEncoder))