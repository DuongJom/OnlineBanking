class User:
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def to_json(self):
        return {
            "name": self.name,
            "address": self.address,
            "phone":self.phone
        }