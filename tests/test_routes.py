import os
import mongomock
import pytest
import json
import openai
from project import app as flask_app
from unittest.mock import patch

os.environ['FLASK_DEBUG'] = 'true'
os.environ['MONGO_URI'] = 'mongodb://mongo:27017/pantry-chef'

mongouri = os.getenv('MONGO_URI', 'mongodb://mongo:27017/pantry-chef')
@mongomock.patch(servers=((mongouri),))

# Define a fixture for the OpenAI API mock when is_recipe is False
@pytest.fixture
def mock_openai_api_message_only():
    # Create a mock response object
    mock_response = {'choices': [{'message': {'content': 'Hello, how are you?'}}]}

    # Use patch to replace openai.ChatCompletion.create with a mock
    with patch.object(openai.ChatCompletion, 'create', return_value=mock_response) as mock_create:
        yield mock_create

# Define a fixture for the OpenAI API mock when is_recipe is True
@pytest.fixture
def mock_openai_api_recipe():
    recipe_response = {
        'title': 'Spaghetti Bolognese',
        'ingredients': ['Spaghetti', 'Tomato Sauce', 'Ground Beef', 'Parmesan'],
        'instructions': ['Cook spaghetti', 'Prepare sauce', 'Serve with parmesan']
    }
    message_content = json.dumps(recipe_response)
    # Create a mock response object
    mock_response = {'choices': [{'message': {'content': message_content}}]}

    # Use patch to replace openai.ChatCompletion.create with a mock
    with patch.object(openai.ChatCompletion, 'create', return_value=mock_response) as mock_create:
        yield mock_create

# Define a fixture for the OpenAI Image API mock when is_recipe is True
@pytest.fixture
def mock_openai_api_image():
    # Use patch to replace openai.Image.create with a mock
    with patch.object(openai.Image, 'create', return_value={'data': [{'url': 'image.png'}]}) as mock_create:
        yield mock_create

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_chat_without_message(client):
    response = client.post('/chat', json={})
    assert response.status_code == 400
    assert 'Missing message parameter' in response.data.decode()

def test_chat_with_empty_message(client):
    response = client.post('/chat', json={'message': ''})
    assert response.status_code == 400
    assert "Message can't be empty" in response.data.decode()

def test_chat_with_message_only(client, mock_openai_api_message_only):
    response = client.post('/chat', json={'message': 'Hello, how are you?'})
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'message' in response_data
    assert response_data['image_url'] == ''

def test_chat_with_message_and_recipe_flag(client, mock_openai_api_recipe, mock_openai_api_image):
    response = client.post('/chat', json={'message': 'Give me a recipe for spaghetti bolognese', 'is_recipe': True})
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'message' in response_data
    assert 'title' in response_data['message']
    assert 'ingredients' in response_data['message']
    assert 'instructions' in response_data['message']
    assert 'image_url' in response_data
    # assert response_data['image_url'] != ''