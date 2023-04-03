from flask import Flask, abort, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize the OpenAI API client
openai.api_key = os.environ['OPENAI_API_KEY']
openai.organization = os.environ['OPENAI_ORG_ID']

# General error handler

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Define a route to handle POST requests
@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not request.json or not 'message' in request.json:
            abort(400, 'Missing message parameter')
        # Get the user message from the request body
        user_message = request.json['message']

        # Generate a response using GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the first generated text from the response
        generated_text = response.choices[0].message.content

        # Return the generated text to the user
        return jsonify({'message': generated_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
