import os
from pymongo import MongoClient
from flask import current_app
from .seeder import seedData
from .utils import parse_object_ids, json_encoder

# Initialize MongoDB client
def initDB():
    try:
        current_app.logger.info("Initializing MongoDB")
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongo:27017/chatbot')
        client = MongoClient(mongo_uri)
        dbClient = client['chatbot']
        return dbClient
    except Exception as e:
        print(f'An error occurred: {e}')
        current_app.logger.error(f'An error occurred: {e}')
    finally:
        current_app.logger.info("chatbot DB client initialized successfully")