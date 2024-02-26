
Image Classification API

    Overview:
This API provides endpoints for classifying images using pre-trained models in PyTorch and TensorFlow. The API is built with FastAPI and is designed to be easy to use and deploy using Docker.

1-Project Structure:
  - app/
    - models/
      - keras.models/
      - pytorch.models/
      - tensorflow.models/
    - routers/
      - keras.py
      - pytorch.py
      - tensorflow.py
    - main.py
  - Dockerfile
  - .gitignore
  - README.txt
  - requirements.txt

  2-Features:
  - Classify images by sending a POST request with an image URL.
  - Support for PyTorch and TensorFlow models.
  - CORS enabled for frontend integration.
  - Docker support for easy deployment.

  3-Requirements:
  - Python 3.8 or later.
  - Dependencies listed in requirements.txt.

  4-Installation:
    1. Clone the repository to your local machine.
    2. Install the required Python packages using `pip install -r requirements.txt`.

  5-Usage:
  - Start the API server with the command `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
  - Access the root endpoint at `http://127.0.0.1:8000` to receive a welcome message.
  - Send a POST request to `/classify/pytorch` or `/classify/tensorflow` with the required JSON payload to classify images.

  6-Endpoints:
  - GET /: Returns a welcome message and confirms that the API is operational.
  - POST /classify/pytorch: Accepts an image URL and returns classification results using the PyTorch model.
  - POST /classify/tensorflow: Accepts an image URL and returns classification results using the TensorFlow model.

  7-Docker:
  - Build the Docker image with `docker build -t image_classification_api .`.
  - Run the API server in a Docker container with `docker run -p 8000:8000 image_classification_api`.

    Note:
  - The PyTorch and TensorFlow models must be placed in their respective directories within the `app/models/` folder.
  - Ensure you have the correct permissions to access and execute the models.