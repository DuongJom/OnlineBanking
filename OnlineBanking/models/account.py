from models import database

db = database.Database().get_db()

class Account():
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def to_json(self):
        return {
            "email": self.email,
            "password": self.password
        }