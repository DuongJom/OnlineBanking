from flask import session
from datetime import datetime
from enums.deleted_type import DeletedType

class BaseModel:
    def __init__(self):
        self.CreatedDate = datetime.now()
        self.CreatedBy = session["current_user"]
        self.ModifiedDate = datetime.now()
        self.ModifiedBy = session["current_user"]
        self.IsDeleted = DeletedType.AVAILABLE.value