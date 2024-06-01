from datetime import datetime
from enums.deleted_type import DeletedType

class BaseModel:
    def __init__(self):
        self.CreatedDate = datetime.now()
        self.CreatedBy = None
        self.ModifiedDate = datetime.now()
        self.ModifiedBy = None
        self.IsDeleted = DeletedType.AVAILABLE.value