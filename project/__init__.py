from flask import Flask, jsonify
from flask_cors import CORS
from project.routes import chatBp, groceriesBp, userBp
from project.db import initDB, seedData
import openai
import os

app = Flask(__name__)
cors = CORS(app)

# Initializes DB client and seeds the database
if os.environ.get('FLASK_ENV') != 'testing':
    with app.app_context():
        dbClient = initDB()
        seedData(dbClient)

# Initialize the OpenAI API client

openai.api_key = os.getenv('OPENAI_API_KEY', '')
openai.organization = os.getenv('OPENAI_ORG_ID', '')

@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

app.register_blueprint(chatBp)
app.register_blueprint(groceriesBp)
app.register_blueprint(userBp)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=os.getenv('FLASK_RUN_PORT', 5000), debug=True)