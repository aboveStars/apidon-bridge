# Model Upload API

This project provides a FastAPI implementation to upload models via a provided URL and save them to a specified path.

## Project Structure

- `app/`: A directory containing the FastAPI application.
  - `main.py`: The main FastAPI application setup with CORS and includes the routers.
  - `routers/`: A directory containing the different routers of the FastAPI application.
    - `upload.py`: Contains the APIRouter for the model upload mechanism.
- `Dockerfile`: Contains the instructions to build a Docker image for the project.
- `requirements.txt`: Lists all the Python dependencies of the project.
- `.gitignore`: Specifies intentionally untracked files to ignore.
- `README.md`: (This file) Includes the documentation of the project.

## Features

- **Model Upload**: Allows users to upload models by providing a `mdl_url` and `mdl_path`.

## Usage

To run the project, you will need Docker installed. Once you have Docker set up, you can build the image and run the container:

```bash
docker build -t model-upload-api .
docker run -p 8000:8000 model-upload-api
```

After running the container, the API will be available at `http://localhost:8000`.

## Endpoints

- POST `/upload/`: Accepts a JSON with `mdl_url` and `mdl_path` to download and save the model.
- GET `/`: Returns a welcome message.

## Using the API with Postman

To test the API endpoints using Postman:

1. Open Postman and create a new request.
2. Set the request method to `POST` for uploading a model.
3. Enter the API URL which will be `http://localhost:8000/upload/` for the upload endpoint.
4. Go to the 'Body' tab, select 'raw', and choose 'JSON' as the format.
5. Enter the JSON data with `mdl_url` and `mdl_path` keys. For example:

```json
{
    "mdl_url": "http://example.com/model.zip",
    "mdl_path": "/path/to/save/model.zip"
}
```

6. Send the request and you should receive a response from the server.
7. For the welcome message, set the request method to `GET` and enter `http://localhost:8000/` as the URL, then send the request.

## Development

To set up a development environment, install the dependencies in `requirements.txt`:

```bash
pip install -r requirements.txt
```

Then, run the application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with live reload for development.

## Deployment

The included Dockerfile is ready for deployment. Build the image, and create a container as shown in the usage section.
