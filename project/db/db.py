import os
from pymongo import MongoClient
from seeder import seedData

# Initialize MongoDB client
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['chatbot']

# Seed JSON data to MongoDB
seedData(db)