from base import BaseModel

class Branch(BaseModel):
	def __init__(self, BranchName, Address):
            self.BranchName = BranchName
            self.Address = Address