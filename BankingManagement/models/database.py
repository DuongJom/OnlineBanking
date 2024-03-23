from pymongo import MongoClient

uri = 'mongodb+srv://admin:admin123@cluster0.w1p8zp5.mongodb.net/?retryWrites=true&w=majority'
class Database:
    def __init__(self):
        # Create a new client and connect to the server
        self.client = MongoClient(uri)
        self.db = self.client['online-banking']
        self.client.admin.command('ping')

    def get_db(self):
        return self.db
    


