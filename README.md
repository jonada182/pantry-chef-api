# Pantry Chef API

A Flask application that uses the [OpenAI Chat API](https://platform.openai.com/docs/guides/chat) for Pantry Chef

## Getting Started

1.  Clone this repository
2.  Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
3.  Set your OpenAI API key and organization ID in the `.env` file:

```
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_ORG_ID=YOUR_ORG_ID
PORT=8000
FLASK_DEBUG=true
```

4.  Run `docker-compose up` to start the application
5.  Open your browser and go to `http://localhost:5001` (or the port you used for `FLASK_PORT`)

## Available Endpoints

-   `/chat` (POST) - Sends a message to OpenAI and receives a response. Expects a JSON request body like this:

```json
{
    "message": "hello, how are you?"
}
``` 

Returns a JSON response with a message from OpenAI:

```json
{
    "message": "I'm fine, thank you. How can I help you?"
}
```

## Environment Variables

This project uses the following environment variables:

### `OPENAI_API_KEY`

The API key for the OpenAI API. This is a required field.

### `OPENAI_ORG_ID`

The organization ID for the OpenAI API. This is a required field.

### `PORT`

The port number that Flask can use to expose the API. (Recommended: 8000)

### `FLASK_DEBUG`

(Recommended: true)

## Learn More

You can learn more about the Chat API in the [OpenAI documentation](https://platform.openai.com/docs/guides/chat)

You can learn more about Flask in the [Flask documentation](https://flask.palletsprojects.com/en/2.1.x/).

You can learn more about Docker Compose in the [Docker documentation](https://docs.docker.com/compose/).

## License

This project is licensed under the MIT License.