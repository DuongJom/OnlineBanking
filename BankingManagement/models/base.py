from datetime import datetime as dt

class BaseModel:
    def __init__(self):
        self.CreatedDate = dt.now()
        self.CreatedBy = None
        self.ModifiedDate = dt.now()
        self.ModifiedBy = None