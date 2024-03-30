from models.base import BaseModel

class LoginMethod(BaseModel):
    def __init__(self, MethodName):
        super().__init__()
        self.MethodName = MethodName

    def to_json(self):
        return {
            "MethodName": self.MethodName
        }