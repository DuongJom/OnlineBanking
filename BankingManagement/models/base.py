from datetime import datetime

class BaseModel:
    def __init__(self):
        self.CreatedDate = datetime.now()
        self.CreatedBy = None
        self.ModifiedDate = datetime.now()
        self.ModifiedBy = None