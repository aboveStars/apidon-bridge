PROJECT

This project is FastAPI that download the image in the url and save it as jpg to new folder(convertedImages)

GETTING STARTED

This section aims to guide you through getting a copy of the project up and running on your local machine for development and testing purposes.

PREREQUISITES

A list of things you need to have installed to run the project.

Raw code
for example,
- Python 3.8+
- FastAPI
- Uvicorn

INSTALLING

Steps to get your development environment running.

Install the required packages.
bash
pip install -r requirements.txt
Run the application locally.
bash
uvicorn orcun.main.convert_jpg:app --reload
This command will start the API at the default address http://127.0.0.1:8000.

USAGE

Some basic actions you can perform with the API and examples of how to access them.

Converting a JPG Image

To convert a JPG image, send a JSON formatted POST request to the corresponding endpoint.

http
POST /convert_jpg/
Content-Type: application/json

{
  "image_url": "http://exampleimage.com/image.jpg"
}

Postman is usable application for sending requests to this api.


Upon a successful request, the image is saved to the specified folder and a response with HTTP status code 200 is returned.

In case of an unsuccesful request, HTTP status code 422 will be throwen.


