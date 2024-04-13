# Unified Model Hosting API

This repository provides a unified API for hosting and classifying images using both custom and pre-trained machine learning models. It combines the `model-hosting` and `preTrained-model-hosting` directories under a shared API framework built with FastAPI.

## Project Structure

- `/model-hosting`: Contains the API for hosting custom ML models.
  - `/app`: Main directory for the FastAPI application.
    - `/models`: Stores the machine learning models by framework.
      - `/pytorch_models`: Contains PyTorch model files (.pth).
      - `/tensorflow_models`: Contains TensorFlow model files (.h5).
      - `/tensorflowlite_models`: Contains TensorFlow Lite model files (.tflite).
    - `/routers`: Contains the API routers defining various endpoints.
      - `tensorflow.py`: Router for TensorFlow image classification.
      - `tensorflow_lite.py`: Router for TensorFlow Lite image classification.
      - `pytorch.py`: Router for PyTorch image classification.
      - `upload.py`: Router for uploading models via URL.
    - `main.py`: Sets up the FastAPI application and includes the routers.
  - `Dockerfile`: Docker configuration for the `model-hosting` service.
  - `requirements.txt`: Specifies the dependencies for the custom model hosting service.

- `/preTrained-model-hosting`: Dedicated to serving pre-trained models.
  - `/app`: Main directory for the FastAPI application.
    - `/routers`: Contains the API routers defining various endpoints.
      - `/pytorch`: Router for PyTorch image classification.
        - `pytorch.py`: Defines the endpoint for image classification using PyTorch models.
        - `imagenet_class_index.json`: Contains the ImageNet class index for PyTorch model predictions.
      - `/tensorflow`: Router for TensorFlow image classification (To be implemented).
        - `tensorflow.py`: Defines the endpoint for image classification using TensorFlow models.
    - `main.py`: FastAPI application initializer for the pre-trained models service.
  - `Dockerfile`: Docker configuration for the `preTrained-model-hosting` service.
  - `requirements.txt`: Specifies the dependencies for the pre-trained model hosting service.

- `/.gitignore`: Configures files and directories to be ignored by Git for the entire repository.
- `/README.md`: Provides documentation and instructions for the entire unified API repository.

## Features

- **Custom Model Hosting**: The `/model-hosting` service allows users to upload and classify images using their own ML models.
- **Pre-Trained Model Hosting**: The `/preTrained-model-hosting`service offers image classification using pre-trained TensorFlow and Pytorch models.

## Endpoints

- POST `/upload/`: Upload a model by providing `model_url` and `model_path`.
- POST `/classify/`: Classify an image using a specified model.
- POST `/classify/tfclassify/`: Classify an image using a specified pre-trained TensorFlow model.
- Post `/classify/ptclassify/`: Classify an image using a specified pre-trained Pytorch model.
- GET `/`: Returns a greeting message and indicates that the API is running.

## Using the API with Postman

To test the API endpoints using Postman:

1. Open Postman and create a new request.
2. Set the request method to `POST` for uploading a model or classifying an image.
3. Enter the API URL `http://localhost:8000/upload/` for the upload endpoint or `http://localhost:8000/classify/` for the classification endpoint or `http://localhost:8000/classify/tfclassify/` for the preTrained TensorFlow model classification endpoint or `http://localhost:8000/classify/ptclassify/` for the preTrained Pytorch model classification endpoint.
4. Go to the 'Headers' tab and set 'Content-Type' to 'application/json'.
5. Go to the 'Body' tab, select 'raw', and choose 'JSON' as the format.

6. Enter the JSON data with the required keys. For example, to upload a model:

```json
{
    "model_url": "http://example.com/model.pth",
    "model_path": "pytorch_models/model_23.pth"
}
```

7. For classifying an image with a PyTorch model:

```json
{
    "image_url": "http://example.com/image.jpg",
    "model_path_url": "model_23.pth"
}
```

8. For classifying an image with a preTrained tensorflow model:

```json
{
    "image_url": "http://example.com/image.jpg",
}
```

9. For classifying an image with a preTrained pytorch model:

```json
{
    "image_url": "http://example.com/image.jpg",
}
```

10. Click on the 'Send' button to make the request. The server's response will be displayed in Postman.

## Usage

To use the services, you need to have Docker installed. Each service within the repository has its own Dockerfile for building and running the API:

### Building and Running model-hosting

```bash
docker build -t model-hosting-api .
docker run -p 8000:8000 model-hosting-api
```

### Building and Running preTrained-model-hosting

```bash
docker build -t pretrained-model-hosting-api .
docker run -p 8000:8000 pretrained-model-hosting-api
```

The APIs for both services can be accessed at `http://localhost:8000` after the containers are up and running.

## Documentation

This README provides all necessary information to understand, set up, and deploy the services. Detailed usage and deployment instructions are included for both `model-hosting` and `preTrained-model-hosting`.

## Conclusion

With this repository, you have a comprehensive solution for model hosting and image classification that caters to both custom and pre-trained models, all within a single, streamlined API system.
