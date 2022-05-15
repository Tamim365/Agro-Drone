import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get('MONGO_URI')
client = MongoClient(db_url)