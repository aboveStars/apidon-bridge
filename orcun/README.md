# Classification API Documentation

Welcome to the Classification API! This API provides various endpoints for classifying images using different models and allows for uploading new models to be used for classification. Below you will find detailed information on how to use each endpoint.

## Authentication

All POST requests require an API key in the request headers under the 'Authorization' title.

Example:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Classify Image

Endpoint to classify an image using a specified model.

**URL:** `/classify`

**Method:** `POST`

**Request Body (form-data):**
- `image_url` (str): URL of the image to be classified.
- `model_path_url` (str): URL where the model is stored.
- `model_extension` (str): The file extension of the model (e.g., .h5, .pth).
- `img_width` (str): Width of image to be classified.
- `img_height` (str): Height of image to be classified.

**Example Request:**
```http
POST /classify HTTP/1.1
Host: api.yourdomain.com
Authorization: Bearer YOUR_API_KEY
Content-Type: multipart/form-data

image_url=https://example.com/image.jpg
model_path_url=https://example.com/model.h5
model_extension=.h5
```

### 2. Upload Model

Endpoint to upload a new model to the API.

**URL:** `/upload_model`

**Method:** `POST`

**Request Body (form-data):**
- `url` (str): URL of the model to be uploaded.
- `path` (str): Location where the model should be saved.
- `label_url` (str): URL of the label file associated with the model.

**Example Request:**
```http
POST /upload_model HTTP/1.1
Host: api.yourdomain.com
Authorization: Bearer YOUR_API_KEY
Content-Type: multipart/form-data

url=https://example.com/new_model.h5
path=/models/new_model.h5
label_url=https://example.com/labels.txt
```

### 3. Classify Image with Pretrained TensorFlow Model

Endpoint to classify an image using a pretrained TensorFlow model.

**URL:** `/pretrained_tensorflow_model`

**Method:** `POST`

**Request Body (form-data):**
- `image_url` (str): URL of the image to be classified.

**Example Request:**
```http
POST /pretrained_tensorflow_model HTTP/1.1
Host: api.yourdomain.com
Authorization: Bearer YOUR_API_KEY
Content-Type: multipart/form-data

image_url=https://example.com/image.jpg
```

### 4. Classify Image with Pretrained PyTorch Model

Endpoint to classify an image using a pretrained PyTorch model.

**URL:** `/pretrained_pytorch_model`

**Method:** `POST`

**Request Body (form-data):**
- `image_url` (str): URL of the image to be classified.

**Example Request:**
```http
POST /pretrained_pytorch_model HTTP/1.1
Host: api.yourdomain.com
Authorization: Bearer YOUR_API_KEY
Content-Type: multipart/form-data

image_url=https://example.com/image.jpg
```

## Response

All endpoints will return a JSON object containing the classification results or the status of the model upload. The structure of the response will vary depending on the endpoint and the operation performed.

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "classification": "cat",
    "confidence": 0.95
  }
}
```

## Error Handling

In case of an error, the API will return an appropriate HTTP status code and a JSON object containing the error message.

**Example Error Response:**
```json
{
  "status": "error",
  "message": "Invalid API key"
}
```

## Contact

For any questions or support, please contact us at support@yourdomain.com.

Thank you for using the Classification API!
