from flask import abort, request, jsonify
from project import app, openai

# Define a route to handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not request.json or not 'message' in request.json:
            abort(400, 'Missing message parameter')
        # Get the user message from the request body
        user_message = request.json['message']

        if user_message == "":
            abort(400, "Message can't be empty")

        # Generate a response using GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Extract the first generated text from the response
        generated_text = response.choices[0].message.content
        generated_text = generated_text.replace('\n', '<br/>')

        # Return the generated text to the user
        return jsonify({'message': generated_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500