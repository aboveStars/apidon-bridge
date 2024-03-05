## TABLE OF CONTENTS
- [APIDON-BRIDGE](#apidon-bridge)
 - [REQUIREMENTS](##requirements)
 -[SETUP AND INSTALLATION](##setup-and-installation)
  -[INSTALL THE NECESSARY PYTHON PACKAGES](###install-the-necessary-python-packages)
  -[START THE FASTAPI SERVER WITH THIS COMMAND](###start-the-fastapi-server-with-this-command)
 -[DOCKER CONTAINER SET-UP](##docker-container-set-up)
  -[HOW TO USE DOCKERFILE](###how-to-use-dockerfile)
 -[MODEL DOWNLOAD AND STORAGE FEATURE](##model-download-and-storage-feature)
  -[HOW TO USE](###how-to-use)
   -[RAW CODE](####raw-code)
   -[TESTING WITH POSTMAN](####testing-with-postman)
 -[CLASSIFY-ENDPOINTS](##classify-endpoints) 
  -[HOW TO USE CLASSIFY](###how-to-use-classify)
   -[RAW CODE](####raw-code-1)
   -[TESTING WITH POSTMAN](####testing-with-postman-1)
 -[KNOWN ISSUES](##known-issues) 
 -[CONCLUSION](#conclusion) 



# APIDON-BRIDGE
APIDON-BRIDGE allows for easy deployment of Pytorch and Tensorflow models with a FastAPI backend, including features like automatic model download and save functionality.
## REQUIREMENTS


Python 3.8 or higher (recommended: 3.10 for optimal compatibility)
FastAPI
An HTTP client for API interaction (e.g., Postman, cURL)


## SETUP AND INSTALLATION

First, clone the repository or download the source code to your local machine. Then, follow these steps to set up your environment:

### INSTALL THE NECESSARY PYTHON PACKAGES
```bash
pip install -r requirements.txt
```
### START THE FASTAPI SERVER WITH THIS COMMAND
```bash
uvicorn hosting.main:app --reload
```
This command starts a local development server that automatically reloads upon any file changes, making it ideal for development purposes.

## DOCKER CONTAINER SET-UP

For deploying APIDON-BRIDGE on a remote server using Docker, use the provided Dockerfile to build and run the container. The Dockerfile contains all necessary instructions to create a containerized environment for the API.


### HOW TO USE DOCKERFILE ###

Follow these steps to build and run your Docker container:

Ensure Docker is installed on your machine.
Navigate to the project directory containing the Dockerfile.
Build the Docker image:
```bash
docker build -t <container-name> .
```
Run the Docker container:
```bash
docker run -d --name -p 8000:8000 <container-name>
```
### DEPLOYMENT ON DIGITAL OCEAN DROPLET WITH BIND-MOUNT###

For deploying APIDON-BRIDGE on a Digital Ocean droplet using Docker and ensuring persistent storage through bind-mount:

Prepare the Droplet:

Install Docker on your Digital Ocean droplet.
Ensure you have SSH access to the droplet.
 Using Bind-Mount:

Identify the local directory on your droplet where you want to persist data.
Utilize Docker's -v or --mount flag to bind-mount the local directory to a directory within the container.
Example command:

```bash
docker run -d --name <container-name> -p 8000:8000 -v /path/on/droplet:/path/in/container -it <image-name>
```
This ensures that data saved in /path/in/container within the container is also accessible in /path/on/droplet on your droplet, facilitating persistent storage and ease of management.



## MODEL DOWNLOAD AND STORAGE FEATURE

APIDON-BRIDGE now includes an API endpoint that allows you to download your Pytorch or Tensorflow model files and save them to a specified directory on your computer. This feature facilitates the management and deployment of machine learning models by providing an automated process for handling model files.

### HOW TO USE

To utilize this feature, make a request to the following endpoint, replacing <model_type> with either pytorch or tensorflow, and specify your desired save location in the request body. 

The endpoint:"http://127.0.0.1:8000/upload_model"

#### RAW CODE
```bash
curl --location 'http://127.0.0.1:8000/upload_model' \
--form 'url="<your_url>"' \
--form 'path="<your_path>"'
```
This API call will download the specified model and save it to the provided directory path on your machine.

#### TESTING WITH POSTMAN

To test the API endpoints using Postman, follow the steps below. Ensure that you select the form-data option when sending POST requests where you need to upload files or specify parameters. Details for each relevant endpoint are provided for clarity.

It is convenient that using the menu in Postman application. First select "Body" option under request bar. Then by using new menu that includes "none,raw,form-data,binary" options, you can send the POST request. 



For the /upload_model endpoint, use the form-data option in Postman. You need to specify the following parameters:

url: The URL where the model file is located.
path: The local directory path where you want to save the model file.

Example cURL command:

```bash
curl --location 'http://127.0.0.1:8000/upload_model' \
--form 'url="https://yourdomain.com/upload/model.pth"' \
--form 'path="/local/path/to/save/model.pth"'
```

## CLASSIFY ENDPOINTS

### HOW TO USE CLASSIFY

You should send the post request the following endpoint by using postman or raw code and you will take predictions of image of models  
The endpoint:"http://127.0.0.1:8000/upload_model"


#### RAW CODE
Example cURL template for classify endpoints:

```bash
curl --location 'http://127.0.0.1:8000/pytorch/classify' \
--form 'image_url="https://yourdomain.com/path/to/image.png"'
```
Be sure to replace pytorch with tensorflow in the URL if you are using the TensorFlow model.



#### TESTING WITH POSTMAN 

For both the /pytorch/classify and /tensorflow/classify endpoints, when sending a POST request, you should use the form-data option and include the parameter named **image_url**. This parameter should contain the URL of the image you wish to classify. When using Postman ,you should follow the same steps with Model Downloading and Storage Feature.





## KNOWN ISSUES


Users may encounter package-related issues when using the Tensorflow model. To avoid these problems, it is recommended to use Python version 3.10 or 3.11.

## CONCLUSION

APIDON-BRIDGE offers a streamlined approach to deploying machine learning models, ensuring ease of access and reliability. The additional feature for downloading and saving model files broadens the utility of the service, making it even more convenient for users managing multiple models. For further assistance or to report issues, please consult the documentation or raise an issue on the project repository.