from flask import Flask, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
cors = CORS(app)

# Initialize the OpenAI API client

openai.api_key = os.getenv('OPENAI_API_KEY', '')
openai.organization = os.getenv('OPENAI_ORG_ID', '')

# General error handler
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

from project import routes
from project.db import dbClient, routes, seedData

# Seed JSON data to MongoDB
seedData(dbClient)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=os.getenv('FLASK_RUN_PORT', 5000), debug=True)