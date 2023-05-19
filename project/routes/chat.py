from flask import Blueprint, current_app, abort, request, jsonify
import time
import json
import openai

# Define the blueprint
chatBp = Blueprint('chat', __name__)

# Define a route to handle chat requests
@chatBp.route('/chat', methods=['POST'])
def chat():
    """
    Parameters:
    - message (string): The prompt message for OpenAI to generate a response
    - is_recipe (bool) If true, the chat will return a JSON with title, ingredientes, and instructions

    Returns: A JSON object with both the `message` and `image_url` generated by OpenAI
    """
    generate_image = False
    is_recipe = False
    if request.json and 'is_recipe' in request.json and request.json['is_recipe'] is True:
        is_recipe = True
        # generate_image = True

    if not request.json or not 'message' in request.json:
        abort(400, 'Missing message parameter')
    # Get the user message from the request body
    user_message = request.json['message']

    if user_message == "":
        abort(400, "Message can't be empty")

    if is_recipe:
        user_message = "JSON Only(title:string, ingredients:string[], instructions:string[]). " + user_message

    current_app.logger.info('Fetching response from OpenAI')

    # start request performance counter 
    start_time = time.perf_counter()

    # Generate a response using GPT
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # log request performance
        request_time = time.perf_counter() - start_time
        current_app.logger.info('Got message from OpenAI in {0:.0f}ms' . format(request_time))

        # Extract the first generated text from the response
        generated_text = response['choices'][0]['message']['content']
    except Exception as e:
        abort(500, e)

    if is_recipe:
        generated_text = generated_text.replace('\n','')
        try:
            generated_text = json.loads(generated_text)
        except:
            current_app.logger.info('Unable to parse JSON from chat response')
            # Return the generated text to the user
            return jsonify({'message': generated_text})

    # Generate an image for the first line of generated_text
    image_url = ''
    try:
        if generate_image and is_recipe and 'title' in generated_text:
            image_response = openai.Image.create(
                prompt=generated_text['title'],
                n=1,
                size="512x512",
            )
            image_url = image_response['data'][0]['url']
    except Exception as e:
        abort(500, e)

    # Return the generated text to the user
    return jsonify({'message': generated_text, 'image_url': image_url})