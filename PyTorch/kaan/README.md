
# Model Upload and Classification API

This project provides a comprehensive API built with FastAPI that allows for model upload and image classification with different machine learning frameworks.

## Project Structure

- `/app`: Main directory for the FastAPI application.
  - `/models`: Contains the machine learning models organized by framework.
    - `/pytorch_models`: Contains PyTorch model files (.pth).
    - `/tensorflow_models`: Contains TensorFlow model files (.h5).
    - `/tensorflowlite_models`: Contains TensorFlow Lite model files (.tflite).
  - `/routers`: Contains the API routers defining various endpoints.
    - `tensorflow.py`: Router for TensorFlow image classification.
    - `tensorflow_lite.py`: Router for TensorFlow Lite image classification.
    - `pytorch.py`: Router for PyTorch image classification.
    - `upload.py`: Router for uploading models via URL.
  - `main.py`: Sets up the FastAPI application, CORS, and includes the routers.
- `Dockerfile`: Contains the instructions to build a Docker image for the API.
- `requirements.txt`: Specifies the Python dependencies of the project.
- `.gitignore`: Configures files and directories to be ignored by Git.
- `README.md`: Provides documentation for the project.

## Features

- **Model Upload**: Endpoint to upload models by providing a URL and save path.
- **Image Classification**: Supports classification for PyTorch, TensorFlow, and TensorFlow Lite models.
- **Modularity**: Separate routers for each machine learning framework for easy maintenance.

## Usage

To use the API, you need to have Docker installed. Build the Docker image and run it with:

```bash
docker build -t model-classify-api .
docker run -p 8000:8000 model-classify-api
```

The API is then accessible at `http://localhost:8000`.

## Endpoints

- POST `/upload/`: Upload a model by providing `mdl_url` and `mdl_path`.
- POST `/classify`: Classify an image using a specified model.
- GET `/`: Returns a greeting message and indicates that the API is running.

## Using the API with Postman

To test the API endpoints using Postman:

1. Open Postman and create a new request.
2. Set the request method to `POST` for uploading a model or classifying an image.
3. Enter the API URL `http://localhost:8000/upload/` for the upload endpoint or the respective classification endpoint.
4. Go to the 'Headers' tab and set 'Content-Type' to 'application/json'.
5. Go to the 'Body' tab, select 'raw', and choose 'JSON' as the format.

6. Enter the JSON data with the required keys. For example, to upload a model:

```json
{
    "mdl_url": "http://example.com/model.pth",
    "mdl_path": "pytorch_models/model_23.pth"
}
```

7. For classifying an image with a PyTorch model:

```json
{
    "image_url": "http://example.com/image.jpg",
    "id_model": "model.pth"
}
```

8. Click on the 'Send' button to make the request. The server's response will be displayed in Postman.

## Development

For development, set up your environment by installing dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Run the application with Uvicorn for hot reload:

```bash
uvicorn app.main:app --reload
```

The API will be live at `http://localhost:8000`, with hot reload enabled for development.

## Deployment

Utilize the included `Dockerfile` for deployment. Build the image and run a container as illustrated in the usage instructions.

Enjoy your model classification and upload tasks with our API!