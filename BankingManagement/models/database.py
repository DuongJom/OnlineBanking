from pymongo import MongoClient 

class Database:
    def __init__(self):
        self.client = MongoClient('mongodb+srv://admin:admin123@cluster0.w1p8zp5.mongodb.net/?retryWrites=true&w=majority')
        self.db = self.client['online-banking']
    def get_db(self):
        return self.db