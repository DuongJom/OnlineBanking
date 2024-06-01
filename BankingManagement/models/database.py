import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
class Database:
    def __init__(self):
        # Create a new client and connect to the server
        self.client = MongoClient(str(os.getenv('MONGODB_URI')))
        self.db = self.client[str(os.getenv('DB_NAME'))]

    def get_db(self):
        return self.db
    


