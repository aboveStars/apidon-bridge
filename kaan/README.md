# Unified Model Hosting API

This repository provides a unified API for hosting and classifying images using both custom and pre-trained machine learning models with parallel processing. It combines the `model-hosting` and `preTrained-model-hosting` directories under a shared API framework built with FastAPI.

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
    - `/utilities`: Contains the API utilities.
      - `middleware.py`: A middleware component that handles API key authentication to secure access to the API endpoints.
    - `main.py`: Sets up the FastAPI application and includes the routers.
  - `Dockerfile`: Docker configuration for the `model-hosting` service.
  - `dockerfile-compose.yml`: Docker configuration for the `model-hosting` service and security.
  - `nginx.conf`: Nginx configuration file that sets up a reverse proxy to handle HTTPS traffic and forward requests to the internal FastAPI application. It includes SSL configuration for secure communication.
  - `requirements.txt`: Specifies the dependencies for the custom model hosting service.

- `/preTrained-model-hosting`: Dedicated to serving pre-trained models.
  - `/app`: Main directory for the FastAPI application.
    - `/routers`: Contains the API routers defining various endpoints.
      - `/pytorch`: Router for PyTorch image classification.
        - `pytorch.py`: Defines the endpoint for image classification using PyTorch models.
        - `imagenet_class_index.json`: Contains the ImageNet class index for PyTorch model predictions.
      - `/tensorflow`: Router for TensorFlow image classification (To be implemented).
        - `tensorflow.py`: Defines the endpoint for image classification using TensorFlow models.
    - `/utilities`: Contains the API utilities.
      - `middleware.py`: A middleware component that handles API key authentication to secure access to the API endpoints.
    - `main.py`: FastAPI application initializer for the pre-trained models service.
  - `Dockerfile`: Docker configuration for the `preTrained-model-hosting` service.
  - `dockerfile-compose.yml`: Docker configuration for the `preTrained-model-hosting` service and security.
  - `nginx.conf`: Nginx configuration file that sets up a reverse proxy to handle HTTPS traffic and forward requests to the internal FastAPI application. It includes SSL configuration for secure communication.
  - `requirements.txt`: Specifies the dependencies for the pre-trained model hosting service.

- `/.gitignore`: Configures files and directories to be ignored by Git for the entire repository.
- `/README.md`: Provides documentation and instructions for the entire unified API repository.

## Features

- **Custom Model Hosting**: The `/model-hosting` service allows users to upload and classify images using their own ML models.
- **Pre-Trained Model Hosting**: The `/preTrained-model-hosting`service offers image classification using pre-trained TensorFlow and Pytorch models with parallel processing for both TensorFlow and PyTorch predictions, improving response time and efficiency.

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
3. Enter the API URL `https://YOUR_DOMAIN/upload/` for the upload endpoint or `https://YOUR_DOMAIN/classify/` for the classification endpoint or `https://YOUR_DOMAIN/classify/tfclassify/` for the preTrained TensorFlow model classification endpoint or `https://YOUR_DOMAIN/classify/ptclassify/` for the preTrained Pytorch model classification endpoint.
4. Go to the 'Headers' tab and set 'Content-Type' to 'application/json'.
5. Go to the 'Body' tab, select 'raw', and choose 'JSON' as the format.
6. Go to the 'Headers' tab and set a key as 'APIKEY' and a value 'YOUR_API_KEY' for verification.

7. Enter the JSON data with the required keys. For example, to upload a model:

```json
{
    "model_url": "http://example.com/model.pth",
    "model_path": "pytorch_models/model_23.pth"
}
```

8. For classifying an image with a PyTorch model:

```json
{
    "image_url": "http://example.com/image.jpg",
    "model_path_url": "model_23.pth"
}
```

9. For classifying an image with a preTrained tensorflow model:

```json
{
    "image_url": "http://example.com/image.jpg",
}
```

10. For classifying an image with a preTrained pytorch model:

```json
{
    "image_url": "http://example.com/image.jpg",
}
```

11. Click on the 'Send' button to make the request. The server's response will be displayed in Postman.

## Usage

To use the services, you need to have Docker and docker-compose installed. Each service within the repository has its own Dockerfile and docker-compose for building and running the API. Before running docker make sure that you have downloaded certbot, nginx and your ssl licenses for more detail you can check [text](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal):

### Nginx Configuration (`nginx.conf`)

#### Overview

This `nginx.conf` file is configured to act as a reverse proxy for our web application. It directs traffic from the web to our application running in a Docker container, managing SSL/TLS for secure HTTPS connections.

#### Configuration Details

- **SSL/TLS Setup**: The configuration includes paths to SSL certificate files (`fullchain.pem` and `privkey.pem`), enabling HTTPS.
- **Proxy Pass**: All HTTP and HTTPS requests to `YOUR_DOMAIN` are forwarded to the internal service `myapp` running on port 8000.
- **Logging**: Access and error logs are directed to standard output and standard error, respectively, making them visible in the Docker logs.

#### Using This Configuration in Your Project

To use this `nginx.conf` in your Docker setup:

1. Ensure the SSL certificates are correctly placed in `/etc/letsencrypt/live/YOUR_DOMAIN/` and readable by the Nginx container.
2. Place `nginx.conf` in your project directory where Docker Compose can access it.
3. Map the configuration file to the Nginx container in your `docker-compose.yml`:

   ```yaml
   volumes:
     - ./nginx.conf:/etc/nginx/nginx.conf
     - /etc/letsencrypt:/etc/letsencrypt:ro
   ```

#### Sample Configuration

Here is a simplified snippet of what the `nginx.conf` might look like:

```nginx
worker_processes 1;

events {
    worker_connections 1024;
}

http {
    sendfile on;

    upstream myapp {
        server myapp:8000;
    }

    server {
        listen 80;
        listen 443 ssl;
        server_name YOUR_DOMAIN;

        ssl_certificate /etc/letsencrypt/live/YOUR_DOMAIN/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/YOUR_DOMAIN/privkey.pem;
    }
}
```

### Building and Running model-hosting

```bash
docker-compose up
```

### Building and Running preTrained-model-hosting

```bash
docker-compose up
```

The APIs for both services can be accessed at `http://YOUR_DOMAIN` after the containers are up and running.

## Documentation

This README provides all necessary information to understand, set up, and deploy the services. Detailed usage and deployment instructions are included for both `model-hosting` and `preTrained-model-hosting`.

## Conclusion

With this repository, you have a comprehensive solution for model hosting and image classification that caters to both custom and pre-trained models, all within a single, streamlined API system with security.
