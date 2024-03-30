from models.base import BaseModel

class Branch(BaseModel):
    def __init__(self, BranchName, Address):
        super().__init__()
        self.BranchName = BranchName
        self.Address = Address or None

    def to_json(self):
        return {
            "BranchName": self.BranchName,
            "Address": self.Address.to_json()
        }