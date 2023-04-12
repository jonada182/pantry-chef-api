import os
from pymongo import MongoClient
from project.db.seeder import seedData

# Initialize MongoDB client
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
dbClient = client['chatbot']