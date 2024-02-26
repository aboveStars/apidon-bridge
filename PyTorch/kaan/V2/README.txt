
# README

## Introduction
This is a machine learning classification API built with FastAPI. It is designed to classify images using either a TensorFlow or PyTorch model. The API accepts an image URL and a model identifier to return the top predictions for the image from the specified model.

## Installation

To run this API, you need to have Python installed on your system. It is recommended to use a virtual environment. Here are the steps to set up the API:

1. Clone the repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To start the API server, run:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables live reloading.

The API has two main endpoints:
- `GET /`: Returns a welcome message.
- `POST /classify`: Accepts a JSON request with an `image_url` and `id_model` to classify the image.

Example `POST` request:

```json
{
    "image_url": "http://example.com/image.jpg",
    "id_model": "model.h5"
}
```

Replace `model.h5` with `model.pth` for PyTorch models.

## API Endpoints

### TensorFlow

- Endpoint: `/tensorflow/classify`
- Method: `POST`
- Body:

```json
{
    "image_url": "http://example.com/image.jpg",
    "id_model": "tensorflow_model.h5"
}
```

### PyTorch

- Endpoint: `/pytorch/classify`
- Method: `POST`
- Body:

```json
{
    "image_url": "http://example.com/image.jpg",
    "id_model": "pytorch_model.pth"
}
```

## Models

Place your TensorFlow and PyTorch models in the respective directories within `app/models`. The TensorFlow models should have an `.h5` extension, and PyTorch models should have a `.pth` extension.

## Requirements

The `requirements.txt` file should contain all the Python packages required for the API. At minimum, it will include:

- fastapi
- pydantic
- uvicorn
- requests
- torch
- torchvision
- tensorflow
- keras
- Pillow

## Docker Support

A `Dockerfile` is included for containerization of the API. To build and run the API in a Docker container, use the following commands:

```bash
docker build -t my_classification_api .
docker run -p 8000:8000 my_classification_api
```

Replace `my_classification_api` with your preferred Docker image name.