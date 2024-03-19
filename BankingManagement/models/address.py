from models.base import BaseModel

class Address(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.Street = kwargs["Street"]
        self.City = kwargs["City"]
        self.Ward = kwargs["Ward"]
        self.Country = kwargs["Country"]
        self.District = kwargs["District"]

    def to_json(self):
        return {
            "Street": self.Street,
            "City": self.City,
            "District": self.District,
            "Ward": self.Ward,
            "Country": self.Country
        }